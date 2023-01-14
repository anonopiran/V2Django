import sys

from django.apps import AppConfig
import logging

logger = logging.getLogger("django.server")


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Users"

    @staticmethod
    def _init_task():
        from Users.models import V2RayProfile, Subscription

        v2r_q = V2RayProfile.objects.all()
        for q_ in v2r_q:
            q_.update__v2ray(force=True)
        V2RayProfile.objects.bulk_update(v2r_q, V2RayProfile.fieldset_v2ray)
        logger.warning(f"{len(v2r_q)} user v2ray updated")
        sub_q = Subscription.update__usage__many(
            {"state": Subscription.StateChoice.ACTIVE}
        )
        logger.warning(f"{len(sub_q)} usages updated")
        u_, _, _, _ = V2RayProfile.update__subscription__many(
            {"subscription__state": Subscription.StateChoice.ACTIVE}
        )
        logger.warning(f"{sum(u_)} user states affected")

    def ready(self):
        from django.conf import settings

        if settings.STATE_INIT_ON_START and (
            "runserver" in sys.argv or "V2Django.wsgi" in sys.argv
        ):
            logger.warning(f"{sys.argv}")
            self._init_task()
