import copy
import re
import socket
from contextlib import contextmanager
from logging import getLogger
from typing import List, Tuple, Union
from uuid import uuid4

import grpc
from django.conf import settings
from google.protobuf import any_pb2
from yarl import URL

import V2RayMan.v2ray_proto.app.proxyman.command.command_pb2 as proxy__pb2
import V2RayMan.v2ray_proto.app.proxyman.command.command_pb2_grpc as proxy__pb2_grpc
import V2RayMan.v2ray_proto.app.stats.command.command_pb2 as log__pb2
import V2RayMan.v2ray_proto.app.stats.command.command_pb2_grpc as log__pb2_grpc
import V2RayMan.v2ray_proto.common.protocol.user_pb2 as user__pb2
import V2RayMan.v2ray_proto.proxy.trojan.config_pb2 as account__trojan__pb2
import V2RayMan.v2ray_proto.proxy.vless.account_pb2 as account__vless__pb2
import V2RayMan.v2ray_proto.proxy.vmess.account_pb2 as account__vmess__pb2
from V2RayMan.config import V2RayConfig

logger = getLogger("vtr")

VTR_CFG = V2RayConfig()


class GrpcClient:
    def __init__(self, servers: list = None):
        self.servers: Tuple[URL] = servers or settings.V2RAY_SERVERS

    @contextmanager
    def grpc_channel(self, channel=None):
        if channel:
            yield channel
            return
        ips = []
        for s_ in self.servers:
            # it is asserted that settings V2RAY_SERVERS is FQDN (in settings)
            ips += [
                f"{x}:{s_.port}" for x in socket.gethostbyname_ex(s_.host)[-1]
            ]
        ips = ",".join(ips)
        ips = "ipv4:" + ips
        with grpc.insecure_channel(ips) as channel:
            yield channel

    def user__stats_all(self, reset=False, channel=None):
        stats = {"downlink": {}, "uplink": {}}

        with self.grpc_channel(channel) as ch_:
            s_ = self._user__stats_all(ch_, reset)
            for k_ in ["downlink", "uplink"]:
                for u_, v_ in s_[k_].items():
                    stats[k_][u_] = stats[k_].get(u_, 0) + v_
        return stats

    def user__add(
        self,
        email,
        tags: Union[List[str], str] = "__all__",
        uuid=None,
        level=0,
        channel=None,
    ):
        uuid = uuid or uuid4()
        if isinstance(tags, str):
            if tags == "__all__":
                tags = [x["tag"] for x in VTR_CFG.iter_inbounds()]
            else:
                tags = [tags]
        with self.grpc_channel(channel) as ch_:
            for t_ in tags:
                p_ = VTR_CFG.get_inbound_protocol(t_)
                self._user__add(
                    ch_,
                    tag=t_,
                    protocol=p_,
                    email=email,
                    uuid=uuid,
                    level=level,
                )
        return {"email": email, "uuid": uuid}

    def user__remove(
        self, email, tags: Union[List[str], str] = "__all__", channel=None
    ):
        if isinstance(tags, str):
            if tags == "__all__":
                tags = [x["tag"] for x in VTR_CFG.iter_inbounds()]
            else:
                tags = [tags]
        with self.grpc_channel(channel) as ch_:
            for t_ in tags:
                p_ = VTR_CFG.get_inbound_protocol(t_)
                self._user__remove(ch_, tag=t_, protocol=p_, email=email)

    @staticmethod
    def _user__stats_all(channel, reset):
        stats = {"downlink": {}, "uplink": {}}
        stub = log__pb2_grpc.StatsServiceStub(channel)
        # noinspection PyUnresolvedReferences
        response = stub.QueryStats(
            log__pb2.QueryStatsRequest(
                reset=reset, regexp=True, pattern="user.+"
            )
        )
        if response.ListFields():
            for s_ in response.ListFields()[0][1]:
                u_, t_ = re.findall(
                    r"user>>>(.+)>>>traffic>>>(.+)", s_.ListFields()[0][1]
                )[0]
                v_ = s_.ListFields()
                if len(v_) <= 1:
                    continue
                v_ = v_[1][1]
                stats[t_][u_] = stats[t_].get(u_, 0) + v_
        return stats

    @staticmethod
    def _user__add(channel, tag: str, protocol: str, email: str, uuid, level):
        if protocol == "vmess":
            account = account__vmess__pb2.Account(id=str(uuid))
        elif protocol == "vless":
            account = account__vless__pb2.Account(id=str(uuid))
        elif protocol == "trojan":
            account = account__trojan__pb2.Account(password=str(uuid))
        else:
            logger.warning(
                f"this operation protocol doesn't support {protocol} protocol in {tag} inbound"
            )
            return
        msg = proxy__pb2.AlterInboundRequest(
            tag=tag,
            operation=to_typed_message(
                proxy__pb2.AddUserOperation(
                    user=user__pb2.User(
                        email=email,
                        level=level,
                        account=to_typed_message(account),
                    )
                )
            ),
        )
        stub = proxy__pb2_grpc.HandlerServiceStub(channel)
        _log_msg = f"inbound tag={tag} - email={email}"
        try:
            stub.AlterInbound(msg)
            logger.info(f"user added ({_log_msg})")
        except grpc.RpcError as rpc_error:
            if rpc_error.details().endswith("already exists."):
                logger.warning(rpc_error.details() + f"({_log_msg})")
            else:
                raise rpc_error

    @staticmethod
    def _user__remove(channel, tag: str, protocol: str, email: str):
        if protocol not in ("vmess", "vless", "trojan"):
            logger.warning(
                f"this operation protocol doesn't support {protocol} protocol in {tag} inbound"
            )
            return
        msg = proxy__pb2.AlterInboundRequest(
            tag=tag,
            operation=to_typed_message(
                proxy__pb2.RemoveUserOperation(email=email)
            ),
        )
        stub = proxy__pb2_grpc.HandlerServiceStub(channel)
        _log_msg = f"inbound tag={tag} - email={email}"
        try:
            stub.AlterInbound(msg)
            logger.info(f"user removed ({_log_msg})")
        except grpc.RpcError as rpc_error:
            if rpc_error.details().endswith("not found."):
                logger.warning(rpc_error.details() + f"({_log_msg})")
            else:
                raise rpc_error


def to_typed_message(message):
    return any_pb2.Any(
        type_url=message.DESCRIPTOR.full_name,
        value=message.SerializeToString(),
    )
