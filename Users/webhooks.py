import logging
from contextlib import contextmanager
from typing import ContextManager, Type

import requests
from django.conf import settings
from django.db.models import Model
from rest_framework.serializers import Serializer
from yarl import URL

logger = logging.getLogger("django.server")


class BaseWebHook:
    url: URL
    serializer: Type[Serializer]

    @contextmanager
    def client(self) -> ContextManager[requests.Session]:
        with requests.Session() as sess_:
            yield sess_

    def send(self, obj: Model):
        if not self.url:
            return
        data = self.serializer(obj).data
        with self.client() as r_:
            try:
                r_.post(self.url, json=data).raise_for_status()
            except (
                requests.exceptions.RequestException,
                requests.exceptions.HTTPError,
            ) as e:
                logger.warning(f"error calling webhook at {self.url}: {e}")


class UserExpireWH(BaseWebHook):
    url = settings.WH_USER_EXPIRE

    def __init__(self) -> None:
        from Users.serializers import V2RayProfileSerializer

        self.serializer = V2RayProfileSerializer
        super().__init__()


class SubscriptionExpireWH(BaseWebHook):
    url = settings.WH_SUBSCRIPTION_EXPIRE

    def __init__(self) -> None:
        from Users.serializers import SubscriptionSerializer

        self.serializer = SubscriptionSerializer
        super().__init__()


class UserActivateWH(BaseWebHook):
    url = settings.WH_SUBSCRIPTION_ACTIVATE

    def __init__(self) -> None:
        from Users.serializers import V2RayProfileSerializer

        self.serializer = V2RayProfileSerializer
        super().__init__()


class SubscriptionActivateWH(BaseWebHook):
    url = settings.WH_SUBSCRIPTION_ACTIVATE

    def __init__(self) -> None:
        from Users.serializers import SubscriptionSerializer

        self.serializer = SubscriptionSerializer
        super().__init__()
