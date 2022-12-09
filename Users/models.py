import datetime
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
import logging

from Utils.models import SignalDisconnect
from Users.webhooks import UserExpireWH, SubscriptionExpireWH

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
        stat_man = StatMan()
        if self.active_subscription:
            s_ = stat_man.get__usage(
                self.email, self.active_subscription.started_at
            )
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
    def status__bandwidth(self) -> bool:
        subs = self.active_subscription
        return (subs is not None) and (
            subs.volume > self.used_bandwidth["total_bytes"]
        )

    @property
    def status__date(self) -> bool:
        subs = self.active_subscription
        return (subs is not None) and (subs.end_date > timezone.now())

    @property
    def active_system(self) -> bool:
        return self.status__date and self.status__bandwidth

    def v2ray__activate(self):
        UserMan().user__add(self.uuid, self.email)

    def v2ray__deactivate(self):
        UserMan().user__rm(self.email)
        UserExpireWH().send(self)

    def update__subscription(self):
        if self.id is None:
            return False
        if not self.active_system:
            with SignalDisconnect(
                (
                    models.signals.post_save,
                    dispatch_subscription_v2rayprofile__update_subscription,
                    Subscription,
                )
            ):
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

    def update__v2ray(self):
        if self.active_system and self.active_admin:
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

    def activate(self):
        self.state = self.StateChoice.ACTIVE
        self.started_at = timezone.now()

    def expire(self):
        if self.state == self.StateChoice.ACTIVE:
            self.state = self.StateChoice.EXPIRE
            SubscriptionExpireWH().send(self)

    @property
    def end_date(self) -> datetime:
        if self.started_at:
            v_ = self.started_at + datetime.timedelta(days=self.duration)
        else:
            v_ = None
        return v_

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


@receiver(pre_delete, sender=Subscription)
def dispatch_subscription__expire(instance: Subscription, **__):
    instance.expire()


@receiver(post_delete, sender=Subscription)
@receiver(post_save, sender=Subscription)
def dispatch_subscription_v2rayprofile__update_subscription(
    instance: Subscription, **__
):
    instance.user.save()
