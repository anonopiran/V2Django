import typing

from django.core.management.base import CommandParser, BaseCommand

from Users.models import Subscription, V2RayProfile

if typing.TYPE_CHECKING:
    _BaseModel = BaseCommand
else:
    _BaseModel = object


class SubsCommandMixin(_BaseModel):
    RESERVES = True
    ACTIVES = True
    EXPIRES = True

    def get_query(self, **options):
        reserve: bool = options.get("reserve", False)
        active: bool = options.get("active", False)
        expire: bool = options.get("expire", False)
        q_ = [
            val
            for cond, val in (
                (reserve, Subscription.StateChoice.RESERVE),
                (active, Subscription.StateChoice.ACTIVE),
                (expire, Subscription.StateChoice.EXPIRE),
            )
            if cond
        ]
        q_ = Subscription.objects.filter(state__in=q_)
        reserve_cnt = q_.filter(state=Subscription.StateChoice.RESERVE).count()
        active_cnt = q_.filter(state=Subscription.StateChoice.ACTIVE).count()
        expire_cnt = q_.filter(state=Subscription.StateChoice.EXPIRE).count()
        self.stdout.write(
            self.style.SUCCESS(
                f"{q_.count()} subscriptions selected "
                f"({reserve_cnt} reserve + {active_cnt} active + {expire_cnt} expire)"
            )
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
        super(SubsCommandMixin, self).handle(*args, **options)


class ProfileCommandMixin(_BaseModel):
    ACTIVES = True
    INACTIVES = True

    def get_query(self, **options):
        active: bool = options.get("active", False)
        inactive: bool = options.get("inactive", False)
        q_ = [val for cond, val in ((active, True), (inactive, False)) if cond]
        q_ = V2RayProfile.objects.filter(v2ray_state__in=q_)
        active_cnt = q_.filter(v2ray_state=True).count()
        inactive_cnt = q_.filter(v2ray_state=False).count()
        self.stdout.write(
            self.style.SUCCESS(
                f"{q_.count()} profiles selected ({active_cnt} active + {inactive_cnt} inactive)"
            )
        )
        return q_

    def add_arguments(self, parser: CommandParser):
        if self.ACTIVES:
            parser.add_argument(
                "--active", action="store_true", help="include active profiles"
            )
        if self.INACTIVES:
            parser.add_argument(
                "--inactive",
                action="store_true",
                help="include inactive profiles",
            )

    def handle(self, *args, **options):
        super(ProfileCommandMixin, self).handle(*args, **options)
