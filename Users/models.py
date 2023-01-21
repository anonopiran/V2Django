from __future__ import annotations

import logging
import uuid
from typing import Optional, Tuple

from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django_fsm import FSMField, transition

import Utils.helpers
from Users.manager import StatMan
from Utils.models import SideEffectMixin
from V2Django.celery import app as celery_app
from tracking_model import TrackingModelMixin
from Upstream.models import Server

logger = logging.getLogger("django.server")


class V2RayProfile(SideEffectMixin, TrackingModelMixin, models.Model):
    email = models.EmailField(unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    active_admin = models.BooleanField(default=True)
    admin_message = models.TextField(blank=True)

    v2ray_state = models.BooleanField(default=False, editable=False)
    v2ray_state_date = models.DateTimeField(
        blank=True, null=True, editable=False
    )

    @property
    def active_subscription(self) -> Optional[Subscription]:
        s_ = self._subscription_state_filter(Subscription.StateChoice.ACTIVE)
        if s_ and s_.exists():
            return s_.get()
        return None

    @property
    def reserve_subscription(self) -> models.QuerySet[Subscription]:
        return self._subscription_state_filter(
            Subscription.StateChoice.RESERVE
        )

    @property
    def expired_subscription(self) -> models.QuerySet[Subscription]:
        return self._subscription_state_filter(Subscription.StateChoice.EXPIRE)

    @property
    def active_or_latest_subscription(self) -> Optional[Subscription]:
        act = self.active_subscription
        if act:
            return act
        exps = self.expired_subscription
        if exps.exists():
            return exps.latest("id")
        return None

    @property
    def active_system(self) -> bool:
        act = self.active_subscription
        return bool(act)

    @property
    def is_active(self) -> bool:
        return self.active_system and self.active_admin

    # ======================== handlers
    def update__subs(self, save=True) -> Optional[Subscription]:
        act = self.active_subscription
        if act:
            logger.debug(
                f"user {self} has an active subscription. doing nothing..."
            )
            return None
        else:
            logger.debug(f"user {self} has not any active subscription")
            res = self.reserve_subscription
            if res.exists():
                act: Subscription = res.earliest("id")
                act.activate()
                logger.info(f"subscription {act} activated for user {self}")
                if save:
                    act.save()
            return act

    def update__v2ray(self, force=False):
        changed = False
        if self.is_active and (not self.v2ray_state or force):
            Server.user__add__many(self.uuid, self.email)
            self.v2ray_state = True
            changed = True
        elif (not self.is_active) and (self.v2ray_state or force):
            Server.user__rm__many(self.email)
            self.v2ray_state = False
            changed = True
        if changed:
            self.v2ray_state_date = timezone.now()
        return changed

    def apply__side_effects(self):
        changes = set()
        if "active_admin" in set(self.tracker.changed.keys()):
            if self.update__v2ray():
                changes.add("v2ray_state")
                changes.add("v2ray_state_date")
        return changes

    @classmethod
    def update__v2ray__many(
        cls, queryset: models.QuerySet[V2RayProfile], force=False
    ):
        flag = []
        for c_, q_ in enumerate(queryset):
            flag.append(q_.update__v2ray(force=force))
        return flag

    # ======================== others
    def __str__(self):
        return self.email

    def _subscription_state_filter(
        self, state
    ) -> models.QuerySet[Subscription]:
        return self.subscription_set.filter(state=state)

    TRACKED_FIELDS = ["active_admin"]


class Subscription(SideEffectMixin, TrackingModelMixin, models.Model):
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
    state = FSMField(
        max_length=1,
        choices=StateChoice.choices,
        default=StateChoice.RESERVE,
        protected=True,
    )
    downlink = models.PositiveBigIntegerField(default=0, editable=False)
    uplink = models.PositiveBigIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True, editable=False)
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

    @property
    def is_expired(self):
        return self.state == self.StateChoice.EXPIRE

    # ======================== handlers
    @transition(
        field=state, source=StateChoice.RESERVE, target=StateChoice.ACTIVE
    )
    def activate(self):
        self.started_at = timezone.now()

    @transition(
        field=state,
        source=[StateChoice.RESERVE, StateChoice.ACTIVE],
        target=StateChoice.EXPIRE,
    )
    def expire(self):
        self.expired_at = timezone.now()
        self.cancel__due_date_notification()
        self.FLAG__JUST_EXPIRED = True

    def update__state(self) -> bool:
        flag = False
        if self.state == self.StateChoice.RESERVE:
            pass
        elif self.state == self.StateChoice.ACTIVE:
            if not (self.calc__status_bandwidth and self.calc__status_date):
                self.expire()
                flag = True
        elif self.state == self.StateChoice.EXPIRE:
            pass
        return flag

    def update__usage(self):
        self.downlink, self.uplink = self.calc__usage

    def update__due_date(self):
        self.due_date = (
            self.started_at + timezone.timedelta(days=self.duration)
            if self.started_at
            else None
        )

    def cancel__due_date_notification(self):
        _uid = self.task_expire_at_due_date_uid
        if _uid:
            celery_app.control.revoke(task_id=_uid)
            self.task_expire_at_due_date_uid = None

    def update__due_date_notification(self):
        task = celery_app.signature("Users.tasks.expire_at_due_date")
        self.cancel__due_date_notification()
        if self.state == self.StateChoice.ACTIVE:
            t_ = task.apply_async(
                (self.id,),
                eta=self.due_date,
            )
            self.task_expire_at_due_date_uid = t_.id

    def apply__side_effects(self):
        changes = set()
        if {"duration", "started_at"}.intersection(
            set(self.tracker.changed.keys())
        ):
            self.update__due_date()
            changes.add("due_date")
        if {"due_date", "volume", "downlink", "uplink"}.intersection(
            set(self.tracker.changed.keys())
        ):
            if self.update__state():
                changes.add("state")
                changes.add("expired_at")
        if "due_date" in set(self.tracker.changed.keys()):
            self.update__due_date_notification()
            changes.add("task_expire_at_due_date_uid")
        return changes

    @classmethod
    def update__usage__many(cls, queryset: models.QuerySet[Subscription]):
        for q_ in queryset:
            q_.update__usage()

    @classmethod
    def update__state__many(cls, queryset: models.QuerySet[Subscription]):
        for q_ in queryset:
            q_.update__state()

    @classmethod
    def update__due_date_notification__many(
        cls, queryset: models.QuerySet[Subscription]
    ):
        for q_ in queryset:
            q_.update__due_date_notification()

    # ======================== others
    def __str__(self):
        return f"{self.id}:{self.user.email}"

    FLAG__JUST_EXPIRED = False
    TRACKED_FIELDS = [
        "duration",
        "started_at",
        "due_date",
        "volume",
        "downlink",
        "uplink",
    ]


# =======================================
# signals
# =======================================
@receiver(models.signals.pre_delete, sender=Subscription)
def _dispatch__subscription__pre_delete(instance: Subscription, **_):
    if instance.state != instance.StateChoice.EXPIRE:
        instance.expire()


@receiver(models.signals.post_save, sender=Subscription)
@receiver(models.signals.post_delete, sender=Subscription)
def _dispatch__subscription__notify_user(
    instance: Subscription, created=None, **_
):
    if created or instance.FLAG__JUST_EXPIRED:
        u = instance.user
        u.update__subs(save=True)
        u.update__v2ray()
        u.save()
