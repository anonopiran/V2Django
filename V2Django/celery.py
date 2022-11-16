import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "V2Django.settings")
app = Celery("v2django")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
