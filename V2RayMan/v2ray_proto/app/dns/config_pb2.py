# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: app/dns/config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from app.router.routercommon import (
    common_pb2 as app_dot_router_dot_routercommon_dot_common__pb2,
)
from common.net import address_pb2 as common_dot_net_dot_address__pb2
from common.net import destination_pb2 as common_dot_net_dot_destination__pb2
from common.protoext import extensions_pb2 as common_dot_protoext_dot_extensions__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14\x61pp/dns/config.proto\x12\x12v2ray.core.app.dns\x1a\x18\x63ommon/net/address.proto\x1a\x1c\x63ommon/net/destination.proto\x1a$app/router/routercommon/common.proto\x1a common/protoext/extensions.proto\"\xb5\x03\n\nNameServer\x12\x30\n\x07\x61\x64\x64ress\x18\x01 \x01(\x0b\x32\x1f.v2ray.core.common.net.Endpoint\x12\x11\n\tclient_ip\x18\x05 \x01(\x0c\x12\x14\n\x0cskipFallback\x18\x06 \x01(\x08\x12I\n\x12prioritized_domain\x18\x02 \x03(\x0b\x32-.v2ray.core.app.dns.NameServer.PriorityDomain\x12\x38\n\x05geoip\x18\x03 \x03(\x0b\x32).v2ray.core.app.router.routercommon.GeoIP\x12\x43\n\x0eoriginal_rules\x18\x04 \x03(\x0b\x32+.v2ray.core.app.dns.NameServer.OriginalRule\x1aV\n\x0ePriorityDomain\x12\x34\n\x04type\x18\x01 \x01(\x0e\x32&.v2ray.core.app.dns.DomainMatchingType\x12\x0e\n\x06\x64omain\x18\x02 \x01(\t\x1a*\n\x0cOriginalRule\x12\x0c\n\x04rule\x18\x01 \x01(\t\x12\x0c\n\x04size\x18\x02 \x01(\r\"w\n\x0bHostMapping\x12\x34\n\x04type\x18\x01 \x01(\x0e\x32&.v2ray.core.app.dns.DomainMatchingType\x12\x0e\n\x06\x64omain\x18\x02 \x01(\t\x12\n\n\x02ip\x18\x03 \x03(\x0c\x12\x16\n\x0eproxied_domain\x18\x04 \x01(\t\"\xe9\x03\n\x06\x43onfig\x12\x38\n\x0bNameServers\x18\x01 \x03(\x0b\x32\x1f.v2ray.core.common.net.EndpointB\x02\x18\x01\x12\x33\n\x0bname_server\x18\x05 \x03(\x0b\x32\x1e.v2ray.core.app.dns.NameServer\x12\x38\n\x05Hosts\x18\x02 \x03(\x0b\x32%.v2ray.core.app.dns.Config.HostsEntryB\x02\x18\x01\x12\x11\n\tclient_ip\x18\x03 \x01(\x0c\x12\x35\n\x0cstatic_hosts\x18\x04 \x03(\x0b\x32\x1f.v2ray.core.app.dns.HostMapping\x12\x0b\n\x03tag\x18\x06 \x01(\t\x12\x14\n\x0c\x64isableCache\x18\x08 \x01(\x08\x12\x39\n\x0equery_strategy\x18\t \x01(\x0e\x32!.v2ray.core.app.dns.QueryStrategy\x12\x17\n\x0f\x64isableFallback\x18\n \x01(\x08\x12\x1e\n\x16\x64isableFallbackIfMatch\x18\x0b \x01(\x08\x1aO\n\nHostsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x30\n\x05value\x18\x02 \x01(\x0b\x32!.v2ray.core.common.net.IPOrDomain:\x02\x38\x01J\x04\x08\x07\x10\x08\"\xdc\x02\n\x10SimplifiedConfig\x12=\n\x0bname_server\x18\x05 \x03(\x0b\x32(.v2ray.core.app.dns.SimplifiedNameServer\x12\x11\n\tclient_ip\x18\x03 \x01(\t\x12\x35\n\x0cstatic_hosts\x18\x04 \x03(\x0b\x32\x1f.v2ray.core.app.dns.HostMapping\x12\x0b\n\x03tag\x18\x06 \x01(\t\x12\x14\n\x0c\x64isableCache\x18\x08 \x01(\x08\x12\x39\n\x0equery_strategy\x18\t \x01(\x0e\x32!.v2ray.core.app.dns.QueryStrategy\x12\x17\n\x0f\x64isableFallback\x18\n \x01(\x08\x12\x1e\n\x16\x64isableFallbackIfMatch\x18\x0b \x01(\x08:\x16\x82\xb5\x18\t\n\x07service\x82\xb5\x18\x05\x12\x03\x64nsJ\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03J\x04\x08\x07\x10\x08\"\x81\x01\n\x15SimplifiedHostMapping\x12\x34\n\x04type\x18\x01 \x01(\x0e\x32&.v2ray.core.app.dns.DomainMatchingType\x12\x0e\n\x06\x64omain\x18\x02 \x01(\t\x12\n\n\x02ip\x18\x03 \x03(\t\x12\x16\n\x0eproxied_domain\x18\x04 \x01(\t\"\xd3\x03\n\x14SimplifiedNameServer\x12\x30\n\x07\x61\x64\x64ress\x18\x01 \x01(\x0b\x32\x1f.v2ray.core.common.net.Endpoint\x12\x11\n\tclient_ip\x18\x05 \x01(\t\x12\x14\n\x0cskipFallback\x18\x06 \x01(\x08\x12S\n\x12prioritized_domain\x18\x02 \x03(\x0b\x32\x37.v2ray.core.app.dns.SimplifiedNameServer.PriorityDomain\x12\x38\n\x05geoip\x18\x03 \x03(\x0b\x32).v2ray.core.app.router.routercommon.GeoIP\x12M\n\x0eoriginal_rules\x18\x04 \x03(\x0b\x32\x35.v2ray.core.app.dns.SimplifiedNameServer.OriginalRule\x1aV\n\x0ePriorityDomain\x12\x34\n\x04type\x18\x01 \x01(\x0e\x32&.v2ray.core.app.dns.DomainMatchingType\x12\x0e\n\x06\x64omain\x18\x02 \x01(\t\x1a*\n\x0cOriginalRule\x12\x0c\n\x04rule\x18\x01 \x01(\t\x12\x0c\n\x04size\x18\x02 \x01(\r*E\n\x12\x44omainMatchingType\x12\x08\n\x04\x46ull\x10\x00\x12\r\n\tSubdomain\x10\x01\x12\x0b\n\x07Keyword\x10\x02\x12\t\n\x05Regex\x10\x03*5\n\rQueryStrategy\x12\n\n\x06USE_IP\x10\x00\x12\x0b\n\x07USE_IP4\x10\x01\x12\x0b\n\x07USE_IP6\x10\x02\x42W\n\x16\x63om.v2ray.core.app.dnsP\x01Z&github.com/v2fly/v2ray-core/v5/app/dns\xaa\x02\x12V2Ray.Core.App.Dnsb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'app.dns.config_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\026com.v2ray.core.app.dnsP\001Z&github.com/v2fly/v2ray-core/v5/app/dns\252\002\022V2Ray.Core.App.Dns'
  _CONFIG_HOSTSENTRY._options = None
  _CONFIG_HOSTSENTRY._serialized_options = b'8\001'
  _CONFIG.fields_by_name['NameServers']._options = None
  _CONFIG.fields_by_name['NameServers']._serialized_options = b'\030\001'
  _CONFIG.fields_by_name['Hosts']._options = None
  _CONFIG.fields_by_name['Hosts']._serialized_options = b'\030\001'
  _SIMPLIFIEDCONFIG._options = None
  _SIMPLIFIEDCONFIG._serialized_options = b'\202\265\030\t\n\007service\202\265\030\005\022\003dns'
  _DOMAINMATCHINGTYPE._serialized_start=2178
  _DOMAINMATCHINGTYPE._serialized_end=2247
  _QUERYSTRATEGY._serialized_start=2249
  _QUERYSTRATEGY._serialized_end=2302
  _NAMESERVER._serialized_start=173
  _NAMESERVER._serialized_end=610
  _NAMESERVER_PRIORITYDOMAIN._serialized_start=480
  _NAMESERVER_PRIORITYDOMAIN._serialized_end=566
  _NAMESERVER_ORIGINALRULE._serialized_start=568
  _NAMESERVER_ORIGINALRULE._serialized_end=610
  _HOSTMAPPING._serialized_start=612
  _HOSTMAPPING._serialized_end=731
  _CONFIG._serialized_start=734
  _CONFIG._serialized_end=1223
  _CONFIG_HOSTSENTRY._serialized_start=1138
  _CONFIG_HOSTSENTRY._serialized_end=1217
  _SIMPLIFIEDCONFIG._serialized_start=1226
  _SIMPLIFIEDCONFIG._serialized_end=1574
  _SIMPLIFIEDHOSTMAPPING._serialized_start=1577
  _SIMPLIFIEDHOSTMAPPING._serialized_end=1706
  _SIMPLIFIEDNAMESERVER._serialized_start=1709
  _SIMPLIFIEDNAMESERVER._serialized_end=2176
  _SIMPLIFIEDNAMESERVER_PRIORITYDOMAIN._serialized_start=480
  _SIMPLIFIEDNAMESERVER_PRIORITYDOMAIN._serialized_end=566
  _SIMPLIFIEDNAMESERVER_ORIGINALRULE._serialized_start=568
  _SIMPLIFIEDNAMESERVER_ORIGINALRULE._serialized_end=610
# @@protoc_insertion_point(module_scope)
