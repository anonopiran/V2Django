import logging
import uuid
from typing import Optional, Tuple

from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils import timezone

import Utils.helpers
from Users.manager import UserMan, StatMan
from V2Django.celery import app as celery_app

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
    def downlink(self) -> int:
        if self.active_or_latest_subscription:
            return self.active_or_latest_subscription.downlink

    @property
    def uplink(self) -> int:
        if self.active_or_latest_subscription:
            return self.active_or_latest_subscription.uplink

    @property
    def due_date(self) -> timezone.datetime:
        if self.active_or_latest_subscription:
            return self.active_or_latest_subscription.due_date

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
    def calc__active_system(self) -> bool:
        return bool(
            self.active_subscription
            and self.active_subscription.calc__status
            == Subscription.StateChoice.ACTIVE
        )

    @property
    def calc__active(self) -> bool:
        return self.calc__active_system and self.active_admin

    @property
    def condition__update_subs(self):
        if self.id is None:  # while being created so no any subs available
            return False
        if (
            not self.calc__active_system
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
    def condition__update_v2ray(self):
        return self.calc__active != self.v2ray_state

    # ======================== handlers
    def v2ray__activate(self):
        UserMan().user__add(self.uuid, self.email)

    def v2ray__deactivate(self):
        UserMan().user__rm(self.email)

    def update__subscription(self, save=True):
        if not self.condition__update_subs:
            return False, None, None
        exp = self.active_subscription
        if exp:
            exp.expire()
            if save:
                exp.save()
        reserve = self.subscription_set.filter(
            state=Subscription.StateChoice.RESERVE
        )
        if reserve.exists():
            res = reserve.earliest("id")
            res.activate()
            if save:
                res.save()
        else:
            res = None
        return True, exp, res

    def update__v2ray(self, force=False):
        if not (self.condition__update_v2ray or force):
            return False
        if self.calc__active:
            self.v2ray__activate()
            self.v2ray_state = True
        else:
            self.v2ray__deactivate()
            self.v2ray_state = False
        self.v2ray_state_date = timezone.now()
        return True

    @classmethod
    def update__subscription__many(cls, query=None, save=True):
        query = query or {}
        qs = cls.objects.filter(**query)
        i_set = []
        e_set = []
        a_set = []
        for q_ in qs:
            i_, e_, a_ = q_.update__subscription(save=False)
            i_set.append(i_)
            e_set.append(e_)
            a_set.append(a_)
        if save:
            e_set_updated = {x for x in e_set if x}
            a_set_updated = {x for x in a_set if x}
            Subscription.objects.bulk_update(
                e_set_updated, Subscription.fieldset_expire
            )
            Subscription.objects.bulk_update(
                a_set_updated, Subscription.fieldset_active
            )
            qs_update = {
                x for i, x in zip(i_set, qs) if i and x.update__v2ray()
            }
            cls.objects.bulk_update(qs_update, cls.fieldset_v2ray)
        return i_set, qs, e_set, a_set

    # ======================== others
    def __str__(self):
        return self.email

    fieldset_v2ray = ["v2ray_state", "v2ray_state_date"]


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
    downlink = models.PositiveBigIntegerField(default=0, editable=False)
    uplink = models.PositiveBigIntegerField(default=0, editable=False)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(blank=True, null=True)
    expired_at = models.DateTimeField(blank=True, null=True)

    task_expire_at_due_date_uid = models.UUIDField(
        null=True, blank=True, editable=False
    )

    @property
    def calc__status_bandwidth(self) -> bool:
        return self.volume > self.downlink + self.uplink

    @property
    def calc__status_date(self) -> bool:
        return self.due_date and self.due_date > timezone.now()

    @property
    def calc__status(self):
        if self.state == self.StateChoice.RESERVE:
            return self.StateChoice.RESERVE
        elif self.calc__status_bandwidth and self.calc__status_date:
            return self.StateChoice.ACTIVE
        else:
            return self.StateChoice.EXPIRE

    @property
    def calc__due_date(self) -> Optional[timezone.datetime]:
        if self.started_at:
            return self.started_at + timezone.timedelta(days=self.duration)
        return None

    @property
    def calc__usage(self) -> Tuple[int, int]:
        _down = 0
        _up = 0
        stat_man = StatMan()
        if self.started_at:
            st = stat_man.get__usage(
                self.user.email, self.started_at, self.expired_at
            )
            for s_ in st:
                if s_["direction"] == "downlink":
                    _down = s_["value"]
                elif s_["direction"] == "uplink":
                    _up = s_["value"]
        return _down, _up

    # ======================== handlers
    def activate(self, force=False):
        if force or self.state == self.StateChoice.RESERVE:
            self.state = self.StateChoice.ACTIVE
            self.started_at = timezone.now()
            self.update__due_date()
            self.expired_at = None

    def expire(self, force=False):
        if force or self.state == self.StateChoice.ACTIVE:
            self.state = self.StateChoice.EXPIRE
            self.expired_at = timezone.now()
            self.cancel__due_date_task()

    def update__usage(self):
        self.downlink, self.uplink = self.calc__usage

    def update__due_date(self):
        self.due_date = self.calc__due_date

    def cancel__due_date_task(self):
        _uid = self.task_expire_at_due_date_uid
        if _uid:
            celery_app.control.revoke(task_id=_uid, terminate=True)
            self.task_expire_at_due_date_uid = None
            return True
        return False

    def update__due_date_task(self):
        task = celery_app.signature("Users.tasks.expire_at_due_date")
        self.cancel__due_date_task()
        if self.state == self.StateChoice.ACTIVE:
            t_ = task.apply_async(
                (self.id,),
                eta=self.due_date,
            )
            self.task_expire_at_due_date_uid = t_.id

    @classmethod
    def update__usage__many(cls, query: dict = None, save=True):
        query = query or {}
        qs = cls.objects.filter(**query)
        for q_ in qs:
            q_.update__usage()
        if save:
            cls.objects.bulk_update(qs, cls.fieldset_usage)
        return qs

    # ======================== others
    def __str__(self):
        return f"{self.id}:{self.user.email}"

    fieldset_active = [
        "state",
        "started_at",
        "due_date",
        "task_expire_at_due_date_uid",
        "expired_at",
    ]
    fieldset_expire = ["state", "expired_at", "task_expire_at_due_date_uid"]
    fieldset_usage = ["downlink", "uplink"]
    fieldset_due_date = ["due_date", "task_expire_at_due_date_uid"]


# ============================================================================================================
# signals
# ============================================================================================================
# @receiver(pre_save, sender=V2RayProfile)
# def dispatch__v2rayprofile__update_subscription(instance: V2RayProfile, **__):
#     instance.update__subscription()
#
#
@receiver(models.signals.pre_save, sender=V2RayProfile)
def dispatch__v2rayprofile__update_v2ray(instance: V2RayProfile, **__):
    instance.update__v2ray()


@receiver(models.signals.pre_save, sender=Subscription)
def dispatch__subscription__update_due_date(instance: Subscription, **__):
    instance.update__due_date()


@receiver(models.signals.post_delete, sender=Subscription)
@receiver(models.signals.post_save, sender=Subscription)
def dispatch__subscription__update_v2rayprofile(
    instance: Subscription, created=None, **__
):
    if created is None or created:
        instance.user.update__subscription(save=True)
        instance.user.save()
