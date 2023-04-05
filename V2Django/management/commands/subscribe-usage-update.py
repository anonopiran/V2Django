import json

from django.core.management.base import BaseCommand
import pika
from django.conf import settings
from Users.models import Subscription

from V2Django.management.commands.Base.Mixins import LoggingCommandMixin


class Command(LoggingCommandMixin, BaseCommand):
    help = "Subscribe to usage update topic"
    logger_name = "subscriber"

    def callback(self, _, __, ___, body):
        logger = self.logger.getChild("callback")
        emails = json.loads(body.decode())
        query = Subscription.objects.filter(
            user__email__in=emails, state=Subscription.StateChoice.ACTIVE
        )
        if len(query) < len(emails):
            logger.warning(
                f"some users don't have active subscription {len(query)} subs vs {len(emails)} selected"
            )
        Subscription.update__usage__many(query)
        expire_cnt = 0
        for q_ in query:
            q_.save()
            logger.debug(f"subscription {q_} usage updated")
            if q_.is_expired:
                logger.debug(f"subscription {q_} expired")
                expire_cnt += 1
        logger.info(f"{len(query)} subscription updated")
        logger.info(f"{expire_cnt} subscription expired")

    def init_channel(self):
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
        return channel, queue_name, exchange

    def handle(self, *args, **options):
        channel, queue_name, exchange = self.init_channel()
        self.stderr.write(
            self.style.WARNING(
                f"start consuming: queue={queue_name} exchange={exchange}"
            )
        )
        channel.start_consuming()
