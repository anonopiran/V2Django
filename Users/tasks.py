from celery import shared_task

from Users.models import V2RayProfile


@shared_task
def task__v2rayprofile_update():
    V2RayProfile.update__all(force=False)
