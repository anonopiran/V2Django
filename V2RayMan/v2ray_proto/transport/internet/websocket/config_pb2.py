# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transport/internet/websocket/config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from common.protoext import extensions_pb2 as common_dot_protoext_dot_extensions__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)transport/internet/websocket/config.proto\x12\'v2ray.core.transport.internet.websocket\x1a common/protoext/extensions.proto\"$\n\x06Header\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\xfe\x01\n\x06\x43onfig\x12\x0c\n\x04path\x18\x02 \x01(\t\x12?\n\x06header\x18\x03 \x03(\x0b\x32/.v2ray.core.transport.internet.websocket.Header\x12\x1d\n\x15\x61\x63\x63\x65pt_proxy_protocol\x18\x04 \x01(\x08\x12\x16\n\x0emax_early_data\x18\x05 \x01(\x05\x12\x1e\n\x16use_browser_forwarding\x18\x06 \x01(\x08\x12\x1e\n\x16\x65\x61rly_data_header_name\x18\x07 \x01(\t:(\x82\xb5\x18\x0b\n\ttransport\x82\xb5\x18\x04\x12\x02ws\x82\xb5\x18\r\x8a\xff)\twebsocketJ\x04\x08\x01\x10\x02\x42\x96\x01\n+com.v2ray.core.transport.internet.websocketP\x01Z;github.com/v2fly/v2ray-core/v5/transport/internet/websocket\xaa\x02\'V2Ray.Core.Transport.Internet.Websocketb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transport.internet.websocket.config_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n+com.v2ray.core.transport.internet.websocketP\001Z;github.com/v2fly/v2ray-core/v5/transport/internet/websocket\252\002\'V2Ray.Core.Transport.Internet.Websocket'
  _CONFIG._options = None
  _CONFIG._serialized_options = b'\202\265\030\013\n\ttransport\202\265\030\004\022\002ws\202\265\030\r\212\377)\twebsocket'
  _HEADER._serialized_start=120
  _HEADER._serialized_end=156
  _CONFIG._serialized_start=159
  _CONFIG._serialized_end=413
# @@protoc_insertion_point(module_scope)
