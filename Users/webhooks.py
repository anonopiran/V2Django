import logging
from abc import abstractmethod

import requests
from celery import shared_task
from django.conf import settings
from yarl import URL

logger = logging.getLogger("django.server")


class BaseWebHook:
    url: URL
    ignore_result = True

    def __init__(self, instance) -> None:
        super().__init__()
        self.instance = instance

    @abstractmethod
    def get_data(self, instance):
        raise NotImplementedError

    def send(self):
        if not self.url:
            return
        data = self.get_data(self.instance)
        _request.delay(url=self.url.__str__(), data=data)


class BaseUserWH:
    @staticmethod
    def get_data(instance):
        from Users.serializers import V2RayProfileSerializer

        return V2RayProfileSerializer(instance).data


class BaseSubscriptionWH:
    @staticmethod
    def get_data(instance):
        from Users.serializers import SubscriptionSerializer

        return SubscriptionSerializer(instance).data


class UserExpireWH(BaseUserWH, BaseWebHook):
    url = settings.WH_USER_EXPIRE


class SubscriptionExpireWH(BaseSubscriptionWH, BaseWebHook):
    url = settings.WH_SUBSCRIPTION_EXPIRE


class UserActivateWH(BaseUserWH, BaseWebHook):
    url = settings.WH_USER_ACTIVATE


class SubscriptionActivateWH(BaseSubscriptionWH, BaseWebHook):
    url = settings.WH_SUBSCRIPTION_ACTIVATE


class UserCreateWH(BaseUserWH, BaseWebHook):
    url = settings.WH_USER_CREATE


class SubscriptionCreateWH(BaseSubscriptionWH, BaseWebHook):
    url = settings.WH_SUBSCRIPTION_CREATE


@shared_task
def _request(url, data):
    with requests.Session() as r_:
        try:
            r_.post(url, json=data).raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.warning(
                f"error calling webhook at {url}: {e.response.json()}"
            )
        except requests.exceptions.RequestException as e:
            logger.warning(f"error calling webhook at {url}: {e}")
