# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transport/internet/config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ftransport/internet/config.proto\x12\x1dv2ray.core.transport.internet\x1a\x19google/protobuf/any.proto\"\x98\x01\n\x0fTransportConfig\x12\x46\n\x08protocol\x18\x01 \x01(\x0e\x32\x30.v2ray.core.transport.internet.TransportProtocolB\x02\x18\x01\x12\x15\n\rprotocol_name\x18\x03 \x01(\t\x12&\n\x08settings\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any\"\xc7\x02\n\x0cStreamConfig\x12\x46\n\x08protocol\x18\x01 \x01(\x0e\x32\x30.v2ray.core.transport.internet.TransportProtocolB\x02\x18\x01\x12\x15\n\rprotocol_name\x18\x05 \x01(\t\x12J\n\x12transport_settings\x18\x02 \x03(\x0b\x32..v2ray.core.transport.internet.TransportConfig\x12\x15\n\rsecurity_type\x18\x03 \x01(\t\x12/\n\x11security_settings\x18\x04 \x03(\x0b\x32\x14.google.protobuf.Any\x12\x44\n\x0fsocket_settings\x18\x06 \x01(\x0b\x32+.v2ray.core.transport.internet.SocketConfig\"7\n\x0bProxyConfig\x12\x0b\n\x03tag\x18\x01 \x01(\t\x12\x1b\n\x13transportLayerProxy\x18\x02 \x01(\x08\"\xb8\x04\n\x0cSocketConfig\x12\x0c\n\x04mark\x18\x01 \x01(\r\x12I\n\x03tfo\x18\x02 \x01(\x0e\x32<.v2ray.core.transport.internet.SocketConfig.TCPFastOpenState\x12\x46\n\x06tproxy\x18\x03 \x01(\x0e\x32\x36.v2ray.core.transport.internet.SocketConfig.TProxyMode\x12%\n\x1dreceive_original_dest_address\x18\x04 \x01(\x08\x12\x14\n\x0c\x62ind_address\x18\x05 \x01(\x0c\x12\x11\n\tbind_port\x18\x06 \x01(\r\x12\x1d\n\x15\x61\x63\x63\x65pt_proxy_protocol\x18\x07 \x01(\x08\x12\x1f\n\x17tcp_keep_alive_interval\x18\x08 \x01(\x05\x12\x18\n\x10tfo_queue_length\x18\t \x01(\r\x12\x1b\n\x13tcp_keep_alive_idle\x18\n \x01(\x05\x12\x16\n\x0e\x62ind_to_device\x18\x0b \x01(\t\x12\x13\n\x0brx_buf_size\x18\x0c \x01(\x03\x12\x13\n\x0btx_buf_size\x18\r \x01(\x03\x12\x16\n\x0e\x66orce_buf_size\x18\x0e \x01(\x08\"5\n\x10TCPFastOpenState\x12\x08\n\x04\x41sIs\x10\x00\x12\n\n\x06\x45nable\x10\x01\x12\x0b\n\x07\x44isable\x10\x02\"/\n\nTProxyMode\x12\x07\n\x03Off\x10\x00\x12\n\n\x06TProxy\x10\x01\x12\x0c\n\x08Redirect\x10\x02*Z\n\x11TransportProtocol\x12\x07\n\x03TCP\x10\x00\x12\x07\n\x03UDP\x10\x01\x12\x08\n\x04MKCP\x10\x02\x12\r\n\tWebSocket\x10\x03\x12\x08\n\x04HTTP\x10\x04\x12\x10\n\x0c\x44omainSocket\x10\x05\x42x\n!com.v2ray.core.transport.internetP\x01Z1github.com/v2fly/v2ray-core/v5/transport/internet\xaa\x02\x1dV2Ray.Core.Transport.Internetb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transport.internet.config_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n!com.v2ray.core.transport.internetP\001Z1github.com/v2fly/v2ray-core/v5/transport/internet\252\002\035V2Ray.Core.Transport.Internet'
  _TRANSPORTCONFIG.fields_by_name['protocol']._options = None
  _TRANSPORTCONFIG.fields_by_name['protocol']._serialized_options = b'\030\001'
  _STREAMCONFIG.fields_by_name['protocol']._options = None
  _STREAMCONFIG.fields_by_name['protocol']._serialized_options = b'\030\001'
  _TRANSPORTPROTOCOL._serialized_start=1206
  _TRANSPORTPROTOCOL._serialized_end=1296
  _TRANSPORTCONFIG._serialized_start=94
  _TRANSPORTCONFIG._serialized_end=246
  _STREAMCONFIG._serialized_start=249
  _STREAMCONFIG._serialized_end=576
  _PROXYCONFIG._serialized_start=578
  _PROXYCONFIG._serialized_end=633
  _SOCKETCONFIG._serialized_start=636
  _SOCKETCONFIG._serialized_end=1204
  _SOCKETCONFIG_TCPFASTOPENSTATE._serialized_start=1102
  _SOCKETCONFIG_TCPFASTOPENSTATE._serialized_end=1155
  _SOCKETCONFIG_TPROXYMODE._serialized_start=1157
  _SOCKETCONFIG_TPROXYMODE._serialized_end=1204
# @@protoc_insertion_point(module_scope)
