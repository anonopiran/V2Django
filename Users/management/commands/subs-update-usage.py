from django.core.management.base import BaseCommand
from Users.models import Subscription

from Users.management.commands.Base.Mixins import SubsCommandMixin


class Command(SubsCommandMixin, BaseCommand):
    help = "Update subscription usages"
    RESERVES = False
    EXPIRES = False

    def handle(self, *args, **options):
        verb = options["verbosity"] > 1
        query = self.get_query(**options)
        Subscription.update__usage__many(query)
        exp = 0
        for q_ in query:
            q_.save()
            if q_.FLAG__JUST_EXPIRED:
                exp += 1
                if verb:
                    self.stdout.write(
                        self.style.NOTICE(f"subscription {q_} expired")
                    )
        self.stdout.write(self.style.SUCCESS(f"{exp} subscriptions expired"))
