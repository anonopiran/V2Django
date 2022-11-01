import datetime
import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

import Utils.helpers
from V2RayMan.api import GrpcClient
from V2RayMan.commands import user__stats__get


class V2RayProfile(models.Model):
    email = models.EmailField(unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    active_system = models.BooleanField(default=False, editable=False)
    active_admin = models.BooleanField(default=True)
    system_message = models.TextField(blank=True, editable=False)
    admin_message = models.TextField(blank=True)

    v2ray_state = models.BooleanField(default=False, editable=False)
    v2ray_state_date = models.DateTimeField(
        blank=True, null=True, editable=False
    )

    @property
    def used_bandwidth(self):
        s_ = user__stats__get(self.email).get(self.email, {})
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
        if self.id:
            s_ = self.subscription_set.order_by("start_date").last()
        else:
            s_ = None
        if s_ is None:
            s_ = type("", (), {})()
            s_.end_volume = 0
            s_.end_date = timezone.datetime(
                1990, 1, 1, tzinfo=timezone.get_current_timezone()
            )
        return s_

    @property
    def status__bandwidth(self):
        subs = self.active_subscription
        return subs.end_volume > self.used_bandwidth["downlink_bytes"]

    @property
    def status__date(self):
        subs = self.active_subscription
        return subs.end_date > timezone.now()

    def v2ray__activate(self, channel=None):
        GrpcClient(servers=settings.V2RAY_SERVERS).user__add(
            email=self.email, uuid=self.uuid, channel=channel
        )

    def v2ray__deactivate(self, channel=None):
        GrpcClient(servers=settings.V2RAY_SERVERS).user__remove(
            email=self.email, channel=channel
        )

    def update__status(self):
        band_ = self.status__bandwidth
        date_ = self.status__date
        msg = []
        if not band_:
            msg.append("bandwidth")
        if not date_:
            msg.append("date")
        self.active_system = band_ and date_
        msg = " - ".join(msg)
        self.system_message = msg

    def update__v2ray(self, channel=None):
        if self.active_system and self.active_admin:
            self.v2ray__activate(channel=channel)
            self.v2ray_state = True
        else:
            self.v2ray__deactivate(channel=channel)
            self.v2ray_state = False
        self.v2ray_state_date = timezone.now()

    def __str__(self):
        return self.email


class Subscription(models.Model):
    user = models.ForeignKey(V2RayProfile, on_delete=models.PROTECT)
    duration = models.IntegerField(default=settings.USER_DEFAULT_SUBS_DURATION)
    volume = models.PositiveBigIntegerField(
        default=Utils.helpers.size__assert_bytes(
            settings.USER_DEFAULT_SUBS_VOLUME
        )
    )
    start_date = models.DateTimeField(auto_now_add=True)
    start_volume = models.PositiveBigIntegerField(blank=True)

    @property
    def end_date(self):
        if self.start_volume is None:
            v_ = None
        else:
            v_ = self.start_date + datetime.timedelta(days=self.duration)
        return v_

    @property
    def end_volume(self):
        if self.start_volume is None:
            v_ = None
        else:
            v_ = self.start_volume + self.volume
        return v_

    def assign__start_volume(self):
        if self.start_volume is None:
            self.start_volume = self.user.used_bandwidth["downlink_bytes"]


# ============================================================================================================
# signals
# ============================================================================================================
@receiver(pre_save, sender=V2RayProfile)
def _v2rayprofile__update_status(instance: V2RayProfile, **__):
    instance.update__status()


@receiver(pre_save, sender=V2RayProfile)
def _v2rayprofile__update_v2ray(instance: V2RayProfile, **__):
    instance.update__v2ray()


@receiver(pre_save, sender=Subscription)
def _subscription__assign__start_volume(instance: Subscription, **__):
    instance.assign__start_volume()


@receiver(post_save, sender=Subscription)
@receiver(post_delete, sender=Subscription)
def subscription__v2rayprofile__update(instance: Subscription, **__):
    instance.user.save()
