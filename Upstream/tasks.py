from uuid import UUID

from celery import shared_task
from celery.utils.log import get_task_logger
from Upstream.manager import UserMan
from yarl import URL
from requests.exceptions import ConnectionError

logger = get_task_logger(__name__)


@shared_task(autoretry_for=(ConnectionError,), max_retries=10, retry_backoff=5)
def add_user(endpoint: URL, uuid: UUID, email):
    UserMan(endpoint=endpoint).user__add(uuid=uuid, email=email)


@shared_task(autoretry_for=(ConnectionError,), max_retries=10, retry_backoff=5)
def rm_user(endpoint: URL, email):
    UserMan(endpoint=endpoint).user__rm(email=email)
