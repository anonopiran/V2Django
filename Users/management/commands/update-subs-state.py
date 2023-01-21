from django.core.management.base import BaseCommand
from Users.models import Subscription


class Command(BaseCommand):
    help = "Update subscription state"

    def handle(self, *args, **options):
        query = Subscription.objects.filter(
            state__in=Subscription.StateChoice.ACTIVE
        )
        Subscription.update__state__many(query)
        count = 0
        for q_ in query:
            q_.save()
            if q_.is_expired:
                count += 1
        self.stdout.write(
            self.style.SUCCESS(f"{count}/{len(query)} state expired")
        )
