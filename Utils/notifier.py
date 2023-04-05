import json
from contextlib import contextmanager
from functools import lru_cache
from typing import ContextManager

import pika
from django.conf import settings


@lru_cache
def _prepare(broker, exchange):
    connection = pika.BlockingConnection(pika.URLParameters(broker))
    channel = connection.channel()
    channel.exchange_declare(
        exchange=exchange,
        exchange_type="topic",
        auto_delete=False,
        durable=True,
    )
    connection.close()


class Notifier:
    def __init__(self):
        self.broker = settings.RABBIT_URI.__str__()
        self.exchange = settings.PUB_EVENT_EXCHANGE
        if self.exchange:
            _prepare(self.broker, self.exchange)

    @contextmanager
    def connection(self) -> ContextManager[pika.BlockingConnection]:
        conn = pika.BlockingConnection(pika.URLParameters(self.broker))
        try:
            yield conn
        finally:
            conn.close()

    def publish(self, topic, body):
        if self.exchange is None:
            return
        body = json.dumps(body)
        with self.connection() as conn:
            conn.channel().basic_publish(
                exchange=self.exchange, routing_key=topic, body=body.encode()
            )
