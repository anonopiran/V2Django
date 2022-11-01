from logging import getLogger

from django.conf import settings

from Utils import helpers
from V2RayMan.api import GrpcClient as V2RayGrpcClient
from V2RayMan.influxdb import Client as InfluxClient

logger = getLogger()
V2RAY_API_CLIENT = V2RayGrpcClient()
INFLUX_CLIENT = InfluxClient()
INFLUX_BUCKET = settings.INFLUX_BUCKET_USER_STATS


def user__stats__store():
    stats = V2RAY_API_CLIENT.user__stats_all(reset=False)
    p_const = {"measurement": "bandwidth"}
    p_ = []
    for i_ in ["uplink", "downlink"]:
        p_ += [
            {
                **p_const,
                "tags": {"user": u_, "direction": i_},
                "fields": {"used": v_},
            }
            for u_, v_ in stats[i_].items()
        ]
    INFLUX_CLIENT.write(INFLUX_BUCKET, p_)
    V2RAY_API_CLIENT.user__stats_all(reset=True)
    logger.info(f"stored {len(p_)} user stats log points")


def user__stats__get(user=None):
    q_ = f"""
    from(bucket:"{INFLUX_BUCKET}")
        |>range(start: -5y)
        |> filter(fn: (r) => r["_measurement"] == "bandwidth")
        {f'|> filter(fn: (r) => r["user"] == "{user}")' if user else ''}
        |> aggregateWindow(every: 5y, fn: sum)
    """
    q_ = INFLUX_CLIENT.query().query(q_)
    result = {}
    for r_ in q_:
        r__ = r_.records[-1]
        u_ = r__.values["user"]
        d_ = r__.values["direction"]
        if u_ not in result.keys():
            result[u_] = {}
        result[u_][d_] = r__.get_value()
    return result
