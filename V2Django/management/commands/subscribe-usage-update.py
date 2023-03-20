import json

from django.core.management.base import BaseCommand
import pika
from django.conf import settings
from Users.models import Subscription
from logging import getLogger

logger = getLogger("django")


class Command(BaseCommand):
    help = "Subscribe to usage update topic"

    @staticmethod
    def callback(_, __, ___, body):
        emails = json.loads(body.decode())
        query = Subscription.objects.filter(
            user__email__in=emails, state=Subscription.StateChoice.ACTIVE
        )
        if len(query) < len(emails):
            logger.warning(
                f"some users don't have active subscription {len(query)} subs vs {len(emails)} selected"
            )
        Subscription.update__usage__many(query)
        for q_ in query:
            q_.save()
            if q_.is_expired:
                logger.info(f"subscription {q_} expired")
        logger.info(f"{len(query)} subscription updated")

    def handle(self, *args, **options):
        connection = pika.BlockingConnection(
            pika.URLParameters(settings.RABBIT_URI.__str__())
        )
        channel = connection.channel()
        exchange = settings.SUB_USAGE_EXCHANGE
        channel.exchange_declare(
            exchange=exchange,
            exchange_type="fanout",
            durable=True,
        )
        queue_name = channel.queue_declare(
            queue="", exclusive=True, auto_delete=True
        ).method.queue
        channel.queue_bind(
            exchange=settings.SUB_USAGE_EXCHANGE, queue=queue_name
        )
        channel.basic_consume(
            queue=queue_name, on_message_callback=self.callback, auto_ack=True
        )
        logger.info(f"start consuming: queue={queue_name} exchange={exchange}")
        channel.start_consuming()
