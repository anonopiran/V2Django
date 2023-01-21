from __future__ import annotations

from contextlib import contextmanager
from typing import ContextManager, TypedDict, Literal, List

from django.conf import settings
from django.utils import timezone
from influxdb_client import InfluxDBClient, QueryApi


class UsageType(TypedDict):
    user: str
    direction: Literal["downlink", "uplink"]
    value: int


class StatMan:
    def __init__(self, uri=None):
        self.url = uri or settings.INFLUX_URI
        self.org = self.url.user
        self.token = self.url.password
        self.bucket = self.url.path.strip("/")
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

    def query_string__usage(self, email, start, stop):
        if isinstance(email, str):
            email = (email,)
        return f"""
            from(bucket:"{self.bucket}")
                |>range(start: {start}s, stop: {stop}s)
                |> filter(fn: (r) => r["_measurement"] == "bandwidth")
                |> filter(fn: (r) => {' or '.join([f'r["user"] == "{e_}"' for e_ in email])} )
                |> group(columns: ["user","direction"], mode: "by")
                |> sum()
            """

    def get__usage(self, email, from_, to_=None) -> List[UsageType]:
        if to_:
            end = int(to_.timestamp() - timezone.now().timestamp())
        else:
            end = 0
        start = int(from_.timestamp() - timezone.now().timestamp())
        start = min(start, -1)
        with self.query() as q_:
            rec = q_.query(self.query_string__usage(email, start, end))
        result: List[UsageType] = [
            {
                "direction": x.records[0].values["direction"],
                "value": x.records[0].get_value(),
                "user": x.records[0].values["user"],
            }
            for x in rec
        ]
        return result
