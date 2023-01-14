import typing
from typing import Tuple, Callable, Type

from django.db.models import Model
from django.dispatch import Signal

from Users import models

if typing.TYPE_CHECKING:
    _BaseModel = Model
else:
    _BaseModel = object


class SignalDisconnect:
    def __init__(self, *args: Tuple[Signal, Callable, Type[Model]]):
        self.signals = args

    def __enter__(self):
        for s_ in self.signals:
            s_[0].disconnect(receiver=s_[1], sender=s_[2])
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        for s_ in self.signals:
            s_[0].connect(receiver=s_[1], sender=s_[2])


class ChangeTrackMixin(_BaseModel):
    change_track: typing.List[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f_ in self.change_track:
            setattr(self, f"_{f_}__old", getattr(self, f_))
