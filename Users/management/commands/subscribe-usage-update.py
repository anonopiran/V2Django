import json

from django.core.management.base import BaseCommand
import redis
from django.conf import settings
from Users.models import Subscription, V2RayProfile


class Command(BaseCommand):
    help = "Subscribe to usage update topic"

    def handle(self, *args, **options):
        _verbose = options["verbosity"] == 2
        r = redis.from_url(settings.REDIS_URI.__str__())
        p = r.pubsub()
        p.psubscribe(settings.SUB_USAGE_UPDATE_TOPIC)
        for message in p.listen():
            if message:
                if isinstance(message["data"], int):
                    print(message)
                    continue
                emails = json.loads(message["data"].decode())
                q_sub = Subscription.update__usage__many(
                    {
                        "user__email__in": emails,
                        "state": Subscription.StateChoice.ACTIVE,
                    },
                    save=True,
                )
                if len(q_sub) != len(emails):
                    self.stdout.write(
                        self.style.WARNING(
                            f"user-subs count mismatch. users:{len(emails)} - subs:{len(q_sub)}"
                        )
                    )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{len(q_sub)} subscriptions usage updated"
                    )
                )
                if _verbose:
                    self.stdout.write(
                        self.style.SUCCESS("\n".join([str(x) for x in q_sub]))
                    )
                i_user, q_user, _, _ = V2RayProfile.update__subscription__many(
                    {"email__in": emails}, save=True
                )
                self.stdout.write(
                    self.style.SUCCESS(f"{sum(i_user)} users state affected")
                )
                if _verbose:
                    self.stdout.write(
                        self.style.SUCCESS(
                            "\n".join(
                                [str(x) for i, x in zip(i_user, q_user) if i]
                            )
                        )
                    )
