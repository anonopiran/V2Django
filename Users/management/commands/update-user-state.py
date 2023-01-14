from django.core.management.base import BaseCommand
from Users.models import Subscription, V2RayProfile


class Command(BaseCommand):
    help = "Update users state"

    def add_arguments(self, parser):
        parser.add_argument(
            "--all",
            action="store_true",
            help="update state of all users (rather than active ones)",
        )

    def handle(self, *args, **options):
        _all = options["all"]
        _verbose = options["verbosity"] == 2
        qu = (
            {}
            if _all
            else {"subscription__state": Subscription.StateChoice.ACTIVE}
        )
        i_, q_, e_, a_ = V2RayProfile.update__subscription__many(qu, True)
        self.stdout.write(self.style.SUCCESS(f"total: {len(i_)}"))
        self.stdout.write(self.style.SUCCESS(f"affected: {sum(i_)}"))
        if _verbose:
            self.stdout.write(
                self.style.SUCCESS(
                    "\n".join({str(x) for i, x in zip(i_, q_) if i})
                )
            )
            self.stdout.write(self.style.SUCCESS("-" * 20))
        e_set = {x for x in e_ if x}
        self.stdout.write(self.style.SUCCESS(f"subs expired: {len(e_set)}"))
        if _verbose:
            self.stdout.write(
                self.style.SUCCESS("\n".join({str(x) for x in e_set}))
            )
            self.stdout.write(self.style.SUCCESS("-" * 20))
        a_set = {x for x in a_ if x}
        self.stdout.write(self.style.SUCCESS(f"subs activated: {len(a_set)}"))
        if _verbose:
            self.stdout.write(
                self.style.SUCCESS("\n".join({str(x) for x in a_set}))
            )
            self.stdout.write(self.style.SUCCESS("-" * 20))
