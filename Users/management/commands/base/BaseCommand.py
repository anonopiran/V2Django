import typing

from django.core.management.base import CommandParser, BaseCommand

from Users.models import Subscription, V2RayProfile

if typing.TYPE_CHECKING:
    _BaseModel = BaseCommand
else:
    _BaseModel = object


class BaseSubsCommand(_BaseModel):
    RESERVES = True
    ACTIVES = True
    EXPIRES = True

    def get_query(self, **options):
        reserve: bool = options.get("reserve", False)
        active: bool = options.get("active", False)
        expire: bool = options.get("expire", False)

        sset = [
            val
            for cond, val in (
                (reserve, Subscription.StateChoice.RESERVE),
                (active, Subscription.StateChoice.ACTIVE),
                (expire, Subscription.StateChoice.EXPIRE),
            )
            if cond
        ]
        q_ = Subscription.objects.filter(state__in=sset)
        self.stdout.write(
            self.style.SUCCESS(f"{q_.count()} subscriptions selected")
        )
        return q_

    def add_arguments(self, parser: CommandParser):
        if self.RESERVES:
            parser.add_argument(
                "--reserve", action="store_true", help="include reserves"
            )
        if self.ACTIVES:
            parser.add_argument(
                "--active", action="store_true", help="include actives"
            )
        if self.EXPIRES:
            parser.add_argument(
                "--expire", action="store_true", help="include expires"
            )

    def handle(self, *args, **options):
        super(BaseSubsCommand, self).handle(*args, **options)


class BaseProfileCommand(_BaseModel):
    ACTIVES = True
    DEACTIVES = True

    def get_query(self, **options):
        active: bool = options.get("active", False)
        deactive: bool = options.get("deactive", False)
        if active and deactive:
            q_ = V2RayProfile.objects.all()
        elif active:
            q_ = V2RayProfile.objects.filter(v2ray_state=True)
        elif deactive:
            q_ = V2RayProfile.objects.filter(v2ray_state=False)
        else:
            q_ = V2RayProfile.objects.all()
        self.stdout.write(
            self.style.SUCCESS(f"{q_.count()} profiles selected")
        )
        return q_

    def add_arguments(self, parser: CommandParser):
        if self.ACTIVES:
            parser.add_argument(
                "--active", action="store_true", help="include actives"
            )
        if self.DEACTIVES:
            parser.add_argument(
                "--deactive", action="store_true", help="include deactives"
            )

    def handle(self, *args, **options):
        super(BaseProfileCommand, self).handle(*args, **options)
