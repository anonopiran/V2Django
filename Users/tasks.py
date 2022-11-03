from celery import shared_task

from Users.commands import user_stats_checkpoint, v2ray_state_update


@shared_task
def user_state_checkpoint_task():
    user_stats_checkpoint()


@shared_task
def v2ray_state_update_task():
    v2ray_state_update()
