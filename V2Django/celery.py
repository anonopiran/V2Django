import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "v2django.settings")
app = Celery("v2django")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
