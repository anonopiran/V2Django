import sys

from django.apps import AppConfig
import logging

logger = logging.getLogger("django.server")


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Users"

    @staticmethod
    def _init_task():
        from Users.models import Subscription

        query = Subscription.objects.filter(
            state=Subscription.StateChoice.ACTIVE
        )
        Subscription.update__usage__many(query)
        for q_ in query:
            q_.save()
            if q_.is_expired:
                logger.info(f"{q_} expired [usage]")
        logger.info(f"{len(query)} usages updated")
        query = Subscription.objects.filter(
            state=Subscription.StateChoice.ACTIVE
        )
        Subscription.update__state__many(query)
        for q_ in query:
            q_.save()
            if q_.is_expired:
                logger.info(f"{q_} expired [due]")

    def ready(self):
        from django.conf import settings

        if settings.STATE_INIT_ON_START and (
            "runserver" in sys.argv or "V2Django.wsgi" in sys.argv
        ):
            logger.warning(f"{sys.argv}")
            self._init_task()
