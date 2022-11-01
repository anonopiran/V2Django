from django.core.management.base import BaseCommand

from V2Django.management.commands.celery_base import (
    BaseCommand as CeleryBaseCommand,
)


class Command(CeleryBaseCommand, BaseCommand):
    help = "Start a celery beats worker"
    _cmd_run = "celery -A V2Django beat"
