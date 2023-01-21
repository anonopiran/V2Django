from django.core.management.base import BaseCommand
from Users.models import Subscription


class Command(BaseCommand):
    help = "Update subscription due date notification task"

    def add_arguments(self, parser):
        parser.add_argument(
            "--all",
            action="store_true",
            help="include expired subscriptions",
        )

    def handle(self, *args, **options):
        _all = options["all"]
        query = Subscription.objects.filter(
            state__in=Subscription.StateChoice.ACTIVE
        )
        if _all:
            query = query.union(
                Subscription.objects.filter(
                    state__in=Subscription.StateChoice.EXPIRE
                )
            )
        Subscription.update__due_date_notification__many(query)
        for q_ in query:
            q_.save()
        self.stdout.write(self.style.SUCCESS(f"{len(query)} tasks updated"))
