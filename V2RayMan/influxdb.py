from typing import List, Union

from django.conf import settings
from influxdb_client import InfluxDBClient


class Client:
    def __init__(self, dsn=None):
        self.dsn = dsn or settings.INFLUX_DSN
        self.org = self.dsn.username
        self.token = self.dsn.password
        self.url = f"{self.dsn.scheme}://{self.dsn.hostname}:{self.dsn.port}"

    @property
    def client(self):
        return InfluxDBClient(url=self.url, token=self.token, org=self.org)

    def write(self, bucket, data: Union[List[dict], dict]):
        cl = self.client
        with cl as cl_:
            with cl_.write_api() as w_:
                w_.write(bucket=bucket, record=data)

    def query(self):
        return self.client.query_api()
