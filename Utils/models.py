from typing import Tuple, List, Any, Callable, Type
from django.dispatch import Signal
from django.db.models import Model


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
