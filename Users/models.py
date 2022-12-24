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
from humanize import naturalsize

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
            res[k_] = naturalsize(0, binary=True)
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
            return exps.latest("id")
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

    # ======================== flags
    @property
    def flag__update_subs(self):
        if self.id is None:  # while being created so no any subs available
            return False
        if (
            not self.active_system
            and self.subscription_set.filter(
                state__in=[
                    Subscription.StateChoice.RESERVE,
                    Subscription.StateChoice.ACTIVE,
                ]
            ).exists()
        ):
            # user is not active but has an active subs (that should not) or has reserved (that should be activated)
            return True
        return False

    @property
    def flag__update_v2ray(self):
        return self.is_active != self.v2ray_state

    # ======================== handlers
    def v2ray__activate(self):
        UserMan().user__add(self.uuid, self.email)
        UserActivateWH(self).send()

    def v2ray__deactivate(self):
        UserMan().user__rm(self.email)
        UserExpireWH(self).send()

    def update__subscription(self, force=False):
        if not (force or self.flag__update_subs):
            return False
        exp = self.active_subscription
        if exp:
            exp.expire()
            with SignalDisconnect(
                (
                    post_save,
                    dispatch__subscription__update_v2rayprofile,
                    Subscription,
                )
            ):
                exp.save()
        reserve = self.subscription_set.filter(
            state=Subscription.StateChoice.RESERVE
        )
        if reserve.exists():
            reserve = reserve.earliest("id")
            reserve.activate()
            with SignalDisconnect(
                (
                    post_save,
                    dispatch__subscription__update_v2rayprofile,
                    Subscription,
                )
            ):
                reserve.save()
        return True

    def update__v2ray(self, force=False):
        if not (force or self.flag__update_v2ray):
            return False
        if self.is_active:
            self.v2ray__activate()
            self.v2ray_state = True
        else:
            self.v2ray__deactivate()
            self.v2ray_state = False
        self.v2ray_state_date = timezone.now()
        return True

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
            flag1 = u_.update__subscription()
            flag2 = u_.update__v2ray()
            if flag1 or flag2:
                update_list.add(u_)
        cls.objects.bulk_update(
            update_list, ["v2ray_state", "v2ray_state_date"]
        )
        logger.info(f"{len(update_list)} users updated")

    # ======================== others
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
    def due_date(self) -> timezone.datetime:
        if self.started_at:
            v_ = self.started_at + timezone.timedelta(days=self.duration)
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
        elif self.state == self.StateChoice.ACTIVE:
            s_ = stat_man.get__usage(self.user.email, self.started_at)
        else:
            s_ = {"downlink": 0, "uplink": 0}
        res = {}
        t_ = 0
        for k_ in ("downlink", "uplink"):
            res[k_ + "_bytes"] = s_.get(k_, 0)
            res[k_] = naturalsize(res[k_ + "_bytes"], binary=True)
            t_ += res[k_ + "_bytes"]
        res["total_bytes"] = t_
        res["total"] = naturalsize(t_, binary=True)
        return res

    @property
    def status__bandwidth(self) -> bool:
        return self.volume > self.usage["total_bytes"]

    @property
    def status__date(self) -> bool:
        return self.due_date > timezone.now()

    # ======================== handlers
    def activate(self, force=False):
        if force or self.state == self.StateChoice.RESERVE:
            self.state = self.StateChoice.ACTIVE
            self.started_at = timezone.now()
            self.expired_at = None
            SubscriptionActivateWH(self).send()

    def expire(self, force=False):
        if force or self.state == self.StateChoice.ACTIVE:
            self.state = self.StateChoice.EXPIRE
            self.expired_at = timezone.now()
            uae = self.usage
            self.usage_at_expire = {
                "downlink": uae["downlink_bytes"],
                "uplink": uae["uplink_bytes"],
            }
            SubscriptionExpireWH(self).send()

    # ======================== others
    def __str__(self):
        return self.user.email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metadata = set()

    meta__disable_update_profile = "dis_signal:update_profile"


# ============================================================================================================
# signals
# ============================================================================================================
@receiver(pre_save, sender=V2RayProfile)
def dispatch__v2rayprofile__update_subscription(instance: V2RayProfile, **__):
    instance.update__subscription()


@receiver(pre_save, sender=V2RayProfile)
def dispatch__v2rayprofile__update_v2ray(instance: V2RayProfile, **__):
    instance.update__v2ray()


@receiver(post_save, sender=V2RayProfile)
def dispatch__v2rayprofile__create_wh(instance: V2RayProfile, created, **__):
    if created:
        UserCreateWH(instance).send()


@receiver(pre_delete, sender=Subscription)
def dispatch__subscription__expire(instance: Subscription, **__):
    instance.expire()


@receiver(post_save, sender=Subscription)
def dispatch__subscription__create_wh(instance: Subscription, created, **__):
    if created:
        SubscriptionCreateWH(instance).send()


@receiver(post_delete, sender=Subscription)
@receiver(post_save, sender=Subscription)
def dispatch__subscription__update_v2rayprofile(instance: Subscription, **__):
    if instance.meta__disable_update_profile not in instance.metadata:
        instance.user.save()
