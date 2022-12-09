from __future__ import annotations

from contextlib import contextmanager
from typing import ContextManager
from uuid import UUID

import requests
from django.conf import settings
from django.utils import timezone
from influxdb_client import InfluxDBClient, QueryApi
from yarl import URL


class StatMan:
    def __init__(self, uri=None):
        self.url = uri or settings.INFLUX_URI
        self.org = self.url.user
        self.token = self.url.password
        self.url = f"{self.url.scheme}://{self.url.host}:{self.url.port}"

    @contextmanager
    def client(self) -> ContextManager[InfluxDBClient]:
        with InfluxDBClient(
            url=self.url, token=self.token, org=self.org
        ) as cl_:
            yield cl_

    @contextmanager
    def query(self) -> ContextManager[QueryApi]:
        with self.client() as cl:
            yield cl.query_api()

    @staticmethod
    def query_string__usage(email, start, stop):
        return f"""
            from(bucket:"{settings.INFLUX_BUCKET_USER_STATS}")
                |>range(start: {start}s, stop: {stop}s)
                |> filter(fn: (r) => r["_measurement"] == "bandwidth")
                |> filter(fn: (r) => r["user"] == "{email}")
                |> sum()
            """

    def get__usage(self, email, from_, to_=None):
        if to_:
            end = int(to_.timestamp() - timezone.now().timestamp())
        else:
            end = 0
        # end = min(end, -1)
        start = int(from_.timestamp() - timezone.now().timestamp())
        start = min(start, -2)
        with self.query() as q_:
            rec = q_.query(self.query_string__usage(email, start, end))
        result = {
            x.records[0].values["direction"]: x.records[0].get_value()
            for x in rec
        }
        return result


class UserMan:
    PATH_ADD = "user"
    PATH_REMOVE = "user"

    def __init__(self, endpoint: URL = None):
        self.endpoint = endpoint or URL(settings.V2USER_URI)

    @contextmanager
    def client(self) -> ContextManager[requests.Session]:
        with requests.Session() as sess_:
            yield sess_

    def user__add(self, uuid: UUID, email: str, level=0):
        data = {"uuid": str(uuid), "email": email, "level": level}
        with self.client() as cl_:
            res = cl_.post(self.endpoint / self.PATH_ADD, json=data)
        res.raise_for_status()

    def user__rm(self, email: str):
        data = {"email": email}
        with self.client() as cl_:
            res = cl_.delete(self.endpoint / self.PATH_REMOVE, json=data)
        res.raise_for_status()
