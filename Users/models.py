import datetime
import json
import logging
import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import (
    post_delete,
    post_save,
    pre_save,
    pre_delete,
)
from django.dispatch import receiver
from django.utils import timezone

import Utils.helpers
from Users.manager import UserMan, StatMan
from Users.webhooks import (
    UserExpireWH,
    SubscriptionExpireWH,
    UserActivateWH,
    SubscriptionActivateWH,
    UserCreateWH,
    SubscriptionCreateWH,
)
from Utils.models import SignalDisconnect

logger = logging.getLogger("django.server")


class V2RayProfile(models.Model):
    email = models.EmailField(unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    active_admin = models.BooleanField(default=True)
    admin_message = models.TextField(blank=True)

    v2ray_state = models.BooleanField(default=False, editable=False)
    v2ray_state_date = models.DateTimeField(
        blank=True, null=True, editable=False
    )

    @property
    def used_bandwidth(self):
        if self.active_or_latest_subscription:
            return self.active_or_latest_subscription.usage
        res = {}
        for k_ in ("downlink", "uplink", "total"):
            res[k_ + "_bytes"] = 0
            res[k_] = Utils.helpers.size__bytes_to_hr(0)
        return res

    @property
    def due_date(self):
        if self.active_or_latest_subscription:
            return self.active_or_latest_subscription.due_date
        return None

    @property
    def active_subscription(self):
        if self.id is None:  # while being created
            return None
        s_ = self.subscription_set.filter(
            state=Subscription.StateChoice.ACTIVE
        )
        if s_.exists():
            return s_.get()
        return None

    @property
    def active_or_latest_subscription(self):
        if self.id is None:  # while being created
            return None
        if self.active_subscription:
            return self.active_subscription
        exps = self.subscription_set.filter(
            state=Subscription.StateChoice.EXPIRE
        )
        if exps.exists():
            return exps.first()
        return None

    @property
    def active_system(self) -> bool:
        return bool(
            self.active_subscription
            and self.active_subscription.status__date
            and self.active_subscription.status__bandwidth
        )

    @property
    def is_active(self) -> bool:
        return self.active_system and self.active_admin

    def v2ray__activate(self):
        UserMan().user__add(self.uuid, self.email)
        UserActivateWH().send(self)

    def v2ray__deactivate(self):
        UserMan().user__rm(self.email)
        UserExpireWH().send(self)

    def update__subscription(self):
        if self.id is None:
            return False
        if not self.active_system:

            exp = self.active_subscription
            if exp:
                exp.expire()
                exp.save()
            reserve = (
                self.subscription_set.filter(
                    state=Subscription.StateChoice.RESERVE
                )
                .order_by("created_at")
                .first()
            )
            if reserve:
                reserve.activate()
                reserve.save()
            return True
        return False

    def update__v2ray(self, force=False):
        _active = self.active_system and self.active_admin
        if force or (_active != self.v2ray_state):
            if _active:
                self.v2ray__activate()
                self.v2ray_state = True
            else:
                self.v2ray__deactivate()
                self.v2ray_state = False
            self.v2ray_state_date = timezone.now()

    @classmethod
    def update__all(cls, force=False):
        if force:
            users = cls.objects.all()
        else:
            users = cls.objects.filter(
                active_admin=True,
                subscription__state=Subscription.StateChoice.ACTIVE,
            )

        update_list = set()
        for u_ in users:
            flag = u_.update__subscription()
            if flag:
                u_.update__v2ray()
                update_list.add(u_)
        cls.objects.bulk_update(
            update_list, ["v2ray_state", "v2ray_state_date"]
        )
        logger.info(f"{len(update_list)} users updated")

    def __str__(self):
        return self.email


class Subscription(models.Model):
    class StateChoice(models.TextChoices):
        RESERVE = "0", "Reserve"
        ACTIVE = "1", "Active"
        EXPIRE = "2", "Expire"

    user = models.ForeignKey(V2RayProfile, on_delete=models.PROTECT)
    duration = models.IntegerField(default=settings.USER_DEFAULT_SUBS_DURATION)
    volume = models.PositiveBigIntegerField(
        default=Utils.helpers.size__assert_bytes(
            settings.USER_DEFAULT_SUBS_VOLUME
        )
    )
    state = models.CharField(
        max_length=1, choices=StateChoice.choices, default=StateChoice.RESERVE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(blank=True, null=True)
    expired_at = models.DateTimeField(blank=True, null=True)
    usage_at_expire = models.JSONField(blank=True, null=True, editable=False)

    @property
    def due_date(self) -> datetime:
        if self.started_at:
            v_ = self.started_at + datetime.timedelta(days=self.duration)
        else:
            v_ = None
        return v_

    @property
    def usage(self) -> json:
        stat_man = StatMan()
        if self.state == self.StateChoice.EXPIRE:
            if self.usage_at_expire:
                s_ = self.usage_at_expire
            else:
                s_ = stat_man.get__usage(
                    self.user.email, self.started_at, self.expired_at
                )
                self.usage_at_expire = s_
                with SignalDisconnect(
                    (
                        models.signals.post_save,
                        dispatch__subscription_v2rayprofile__update_subscription,
                        Subscription,
                    )
                ):
                    self.save(update_fields=["usage_at_expire"])

        elif self.state == self.StateChoice.ACTIVE:
            s_ = stat_man.get__usage(self.user.email, self.started_at)
        else:
            s_ = {"downlink": 0, "uplink": 0}
        res = {}
        t_ = 0
        for k_ in ("downlink", "uplink"):
            res[k_ + "_bytes"] = s_.get(k_, 0)
            res[k_] = Utils.helpers.size__bytes_to_hr(res[k_ + "_bytes"])
            t_ += res[k_ + "_bytes"]
        res["total_bytes"] = t_
        res["total"] = Utils.helpers.size__bytes_to_hr(t_)
        return res

    @property
    def status__bandwidth(self) -> bool:
        return self.volume > self.usage["total_bytes"]

    @property
    def status__date(self) -> bool:
        return self.due_date > timezone.now()

    def activate(self):
        self.state = self.StateChoice.ACTIVE
        self.started_at = timezone.now()
        self.expired_at = None
        SubscriptionActivateWH().send(self)

    def expire(self):
        if self.state == self.StateChoice.ACTIVE:
            self.state = self.StateChoice.EXPIRE
            self.expired_at = timezone.now()
            SubscriptionExpireWH().send(self)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.user.email


# ============================================================================================================
# signals
# ============================================================================================================
@receiver(pre_save, sender=V2RayProfile)
def dispatch__v2rayprofile__update_subscription(instance: V2RayProfile, **__):
    instance.update__subscription()


@receiver(pre_save, sender=V2RayProfile)
def dispatch__v2rayprofile__update_v2ray(instance: V2RayProfile, **__):
    instance.update__v2ray()


@receiver(pre_save, sender=V2RayProfile)
def dispatch__v2rayprofile__create_wh_flag(instance: V2RayProfile, **__):
    if instance.id is None:
        instance.create_wh_flag = True


@receiver(post_save, sender=V2RayProfile)
def dispatch__v2rayprofile__create_wh(instance: V2RayProfile, **__):
    if getattr(instance, "create_wh_flag", False):
        UserCreateWH().send(instance)


@receiver(pre_save, sender=Subscription)
def dispatch__subscription__create_wh_flag(instance: Subscription, **__):
    if instance.id is None:
        instance.create_wh_flag = True


@receiver(pre_delete, sender=Subscription)
def dispatch__subscription__expire(instance: Subscription, **__):
    instance.expire()


@receiver(post_delete, sender=Subscription)
@receiver(post_save, sender=Subscription)
def dispatch__subscription__create_wh(instance: Subscription, **__):
    if getattr(instance, "create_wh_flag", False):
        SubscriptionCreateWH().send(instance)


@receiver(post_save, sender=Subscription)
def dispatch__subscription_v2rayprofile__update_subscription(
    instance: Subscription, **__
):
    instance.user.save()
