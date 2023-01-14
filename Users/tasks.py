from celery import shared_task
from celery.utils.log import get_task_logger

from Users.models import Subscription

logger = get_task_logger(__name__)


@shared_task
def expire_at_due_date(subs_id):
    s_ = Subscription.objects.get(id=subs_id)
    u_ = s_.user
    i_, o_, n_ = u_.update__subscription(save=True)
    u_.save()
    if i_:
        logger.info(
            f"user {u_} state updated: old-subs:{o_} new-subs:{n_} v2ray:{u_.v2ray_state}"
        )
    else:
        logger.warning(f"user {u_} due date didn't affect state!")
