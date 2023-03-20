import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "V2Django.settings")
app = Celery("v2django")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.task_routes = {
    "Users.tasks.expire_at_due_date": {"queue": "long_duedate_tasks"},
    "Upstream.tasks.*": {"queue": "f2u_tasks"},
}
app.autodiscover_tasks()
