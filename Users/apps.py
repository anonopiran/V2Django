import sys

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Users"

    def ready(self):
        from django.conf import settings

        from Users.models import V2RayProfile

        if (
            settings.USER_INIT_ON_START
            and ("manage.py" not in sys.argv[0] or sys.argv[1] == "runserver")
            and "celery" not in sys.argv[0]
        ):
            V2RayProfile.update__all(force=True)
