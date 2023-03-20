import typing
from abc import abstractmethod
from functools import cached_property

from django.db.models import Model, signals
from django.dispatch import receiver

from Utils.notifier import Notifier

if typing.TYPE_CHECKING:
    _BaseModel = Model
else:
    _BaseModel = object


class SideEffectMixin(_BaseModel):
    @abstractmethod
    def apply__side_effects(self) -> set:
        raise NotImplementedError


class NotifierMixin(_BaseModel):
    notifications: list = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notifications = []

    @cached_property
    def notifier(self):
        return Notifier()

    def add_notification(self, topic, data):
        self.notifications = self.notifications or []
        self.notifications.append({"topic": topic, "body": data})


@receiver(signals.pre_save)
def _dispatch__side_effect_mixin__pre_save(
    sender, instance: SideEffectMixin, update_fields: list, **_
):
    if not issubclass(sender, SideEffectMixin):
        return
    f_ = instance.apply__side_effects()
    if update_fields:
        update_fields.extend(f_ - set(update_fields))


@receiver(signals.post_save)
@receiver(signals.post_delete)
def _dispatch__notifier_mixin__post_save(sender, instance: NotifierMixin, **_):
    if not issubclass(sender, NotifierMixin):
        return
    for n_ in instance.notifications:
        instance.notifier.publish(n_["topic"], n_["body"])
