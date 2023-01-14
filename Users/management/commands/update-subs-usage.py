from django.core.management.base import BaseCommand
from Users.models import Subscription


class Command(BaseCommand):
    help = "Update subscription usage"

    def add_arguments(self, parser):
        parser.add_argument(
            "--all",
            action="store_true",
            help="include expired subscriptions",
        )

    def handle(self, *args, **options):
        _all = options["all"]
        _verbose = options["verbosity"] == 2
        q = (
            dict(
                state__in=[
                    Subscription.StateChoice.ACTIVE,
                    Subscription.StateChoice.EXPIRE,
                ]
            )
            if _all
            else dict(state=Subscription.StateChoice.ACTIVE)
        )
        q_usage = Subscription.update__usage__many(q, save=True)
        self.stdout.write(self.style.SUCCESS(f"{len(q_usage)} usages updated"))
        if _verbose:
            self.stdout.write(
                self.style.SUCCESS("\n".join([str(x) for x in q_usage]))
            )
