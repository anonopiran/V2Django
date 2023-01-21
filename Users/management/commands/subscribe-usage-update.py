import json

from django.core.management.base import BaseCommand
import pika
from django.conf import settings
from Users.models import Subscription


class Command(BaseCommand):
    help = "Subscribe to usage update topic"

    def callback(self, _, __, ___, body):
        emails = json.loads(body.decode())
        query = Subscription.objects.filter(
            user__email__in=emails, state=Subscription.StateChoice.ACTIVE
        )
        if len(query) < len(emails):
            self.stdout.write(
                self.style.WARNING(
                    f"some users don't have active subscription {len(query)} vs {len(emails)}"
                )
            )
        Subscription.update__usage__many(query)
        for q_ in query:
            q_.save()
            if q_.is_expired:
                self.stdout.write(
                    self.style.SUCCESS(f"subscription {q_} expired")
                )
        self.stdout.write(
            self.style.SUCCESS(f"{len(query)} subscription updated")
        )

    def handle(self, *args, **options):
        connection = pika.BlockingConnection(
            pika.URLParameters(settings.RABBIT_URI.__str__())
        )
        channel = connection.channel()
        channel.exchange_declare(
            exchange=settings.SUB_USAGE_EXCHANGE,
            exchange_type="fanout",
            durable=True,
        )
        queue_name = channel.queue_declare(
            queue="", exclusive=True
        ).method.queue
        channel.queue_bind(
            exchange=settings.SUB_USAGE_EXCHANGE, queue=queue_name
        )
        channel.basic_consume(
            queue=queue_name, on_message_callback=self.callback, auto_ack=True
        )
        channel.start_consuming()
