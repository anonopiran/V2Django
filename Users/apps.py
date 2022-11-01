from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Users"

    def ready(self):
        from django.conf import settings

        from Users.commands import v2ray_state_update

        if settings.USER_INIT_ON_START:
            v2ray_state_update()
