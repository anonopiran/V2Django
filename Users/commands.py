from Users.models import V2RayProfile
from V2RayMan.api import GrpcClient
from V2RayMan.commands import user__stats__store


def user_state_checkpoint():
    user__stats__store()


def v2ray_state_update():
    # todo: optimize (just update users who needed to be, unless forced)
    with GrpcClient().grpc_channel() as ch_:
        all_users = V2RayProfile.objects.all()
        for u_ in all_users:
            u_.update__status()
            u_.update__v2ray(channel=ch_)
    V2RayProfile.objects.bulk_update(
        all_users,
        ["active_system", "system_message", "v2ray_state", "v2ray_state_date"],
    )
