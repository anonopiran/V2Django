import datetime
import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

import Utils.helpers
from Users.manager import UserMan, StatMan
import logging

logger = logging.getLogger("django.server")


class V2RayProfile(models.Model):
    email = models.EmailField(unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    active_system = models.BooleanField(default=False, editable=False)
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
                self.email, self.active_subscription.start_date
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
        if self.id:
            s_ = self.subscription_set.order_by("id").last()
        else:
            s_ = None
        return s_

    @property
    def status__bandwidth(self):
        subs = self.active_subscription
        return (subs is not None) and (
            subs.volume > self.used_bandwidth["total_bytes"]
        )

    @property
    def status__date(self):
        subs = self.active_subscription
        return (subs is not None) and (subs.end_date > timezone.now())

    def v2ray__activate(self):
        UserMan().user__add(self.uuid, self.email)

    def v2ray__deactivate(self):
        UserMan().user__rm(self.email)

    def update__status(self):
        band_ = self.status__bandwidth
        date_ = self.status__date
        self.active_system = band_ and date_

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
            users = cls.objects.filter(active_admin=True, active_system=True)
        s_ = users.values("active_admin", "active_system")
        update_list = set()
        for s_, u_ in zip(s_, users):
            u_.update__status()
            if (
                force
                or u_.active_admin != s_["active_admin"]
                or u_.active_system != s_["active_system"]
            ):
                u_.update__v2ray()
                update_list.add(u_)
        cls.objects.bulk_update(
            update_list, ["active_system", "v2ray_state", "v2ray_state_date"]
        )
        logger.info(f"{len(update_list)} users updated")

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

    @property
    def end_date(self):
        v_ = self.start_date + datetime.timedelta(days=self.duration)
        return v_

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.user.email


# ============================================================================================================
# signals
# ============================================================================================================
@receiver(pre_save, sender=V2RayProfile)
def _v2rayprofile__update_status(instance: V2RayProfile, **__):
    instance.update__status()


@receiver(pre_save, sender=V2RayProfile)
def _v2rayprofile__update_v2ray(instance: V2RayProfile, **__):
    instance.update__v2ray()


@receiver(post_save, sender=Subscription)
@receiver(post_delete, sender=Subscription)
def _subscription__v2rayprofile__update(instance: Subscription, **__):
    instance.user.save()
