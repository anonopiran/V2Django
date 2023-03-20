from django.core.management.base import BaseCommand
from Users.models import Subscription

from Users.management.commands.base.BaseCommand import BaseSubsCommand


class Command(BaseSubsCommand, BaseCommand):
    help = "Update subscription usages"
    RESERVES = False

    def handle(self, *args, **options):
        query = self.get_query(**options)
        Subscription.update__usage__many(query)
        exp = 0
        for q_ in query:
            q_.save()
            exp += q_.FLAG__JUST_EXPIRED
        self.stdout.write(self.style.WARNING(f"{exp} subscriptions expired"))
