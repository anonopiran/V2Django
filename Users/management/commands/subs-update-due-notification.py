from django.core.management.base import BaseCommand

from Users.management.commands.Base.Mixins import SubsCommandMixin


class Command(SubsCommandMixin, BaseCommand):
    help = "Update subscription due date notification"
    RESERVES = False
    EXPIRES = False

    def handle(self, *args, **options):
        query = self.get_query(**options)
        for q_ in query:
            q_.update__due_date_notification()
            q_.save()
