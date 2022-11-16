from django.core.management.base import BaseCommand
from Users.models import V2RayProfile


class Command(BaseCommand):
    help = "Update all users status"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force to update all users (rather than just active ones)",
        )

    def handle(self, *args, **options):
        V2RayProfile.update__all(force=options["force"])
