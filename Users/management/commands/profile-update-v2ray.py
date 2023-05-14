from django.core.management import CommandParser
from django.core.management.base import BaseCommand

from Users.management.commands.Base.Mixins import ProfileCommandMixin
from Upstream.models import Server


class Command(ProfileCommandMixin, BaseCommand):
    help = "Update profiles v2ray status"

    def add_arguments(self, parser: CommandParser):
        super().add_arguments(parser)
        parser.add_argument(
            "--servers",
            nargs="*",
            help="servers [id] to forcibly apply users",
            default=None,
        )

    def handle(self, *args, **options):
        query = self.get_query(**options)
        srv = options.get("servers")
        srv = (
            Server.objects.filter(id__in=srv) if srv else Server.objects.all()
        )
        self.stdout.write(
            self.style.SUCCESS(
                "selected:\n{}".format("\n".join([str(x) for x in srv]))
            )
        )
        if input("proceed?[y,N]").lower() != "y":
            return
        for q_ in query:
            if q_.v2ray_state:
                Server.user__add__many(
                    uuid=q_.uuid, email=q_.email, queryset=srv
                )
            else:
                Server.user__rm__many(email=q_.email, queryset=srv)
