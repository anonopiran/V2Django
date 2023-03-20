from django.core.management.base import BaseCommand

from Users.management.commands.base.BaseCommand import BaseProfileCommand


class Command(BaseProfileCommand, BaseCommand):
    help = "Update profiles v2ray status"

    def handle(self, *args, **options):
        query = self.get_query(**options)
        for q_ in query:
            q_.update__v2ray(force=True)
