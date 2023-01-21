from celery import shared_task
from celery.utils.log import get_task_logger

from Users.models import Subscription

logger = get_task_logger(__name__)


@shared_task
def expire_at_due_date(subs_id):
    s_ = Subscription.objects.get(id=subs_id)
    if s_.is_expired:
        logger.warning(f"subs {s_} is already expired!")
    else:
        s_.update__state()
        if not s_.is_expired:
            logger.warning(
                f"subs {s_} didn't expire at due date! creating new task"
            )
            s_.update__due_date_notification()
        else:
            logger.info(f"subs {s_} expired")
        s_.save()
