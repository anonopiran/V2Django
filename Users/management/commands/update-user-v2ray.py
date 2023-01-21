from django.core.management.base import BaseCommand

from Users.models import V2RayProfile


class Command(BaseCommand):
    help = "Update subscription usage"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="force to reassign state",
        )

    def handle(self, *args, **options):
        _force = options["force"]
        query = V2RayProfile.objects.all()
        updated = V2RayProfile.update__v2ray__many(query, _force)
        for q_, u_ in zip(query, updated):
            if u_:
                q_.save()
        self.stdout.write(self.style.SUCCESS(f"{sum(updated)} users updated"))
