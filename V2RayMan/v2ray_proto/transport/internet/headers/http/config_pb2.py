# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transport/internet/headers/http/config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,transport/internet/headers/http/config.proto\x12*v2ray.core.transport.internet.headers.http\"%\n\x06Header\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x03(\t\"\x18\n\x07Version\x12\r\n\x05value\x18\x01 \x01(\t\"\x17\n\x06Method\x12\r\n\x05value\x18\x01 \x01(\t\"\xea\x01\n\rRequestConfig\x12\x44\n\x07version\x18\x01 \x01(\x0b\x32\x33.v2ray.core.transport.internet.headers.http.Version\x12\x42\n\x06method\x18\x02 \x01(\x0b\x32\x32.v2ray.core.transport.internet.headers.http.Method\x12\x0b\n\x03uri\x18\x03 \x03(\t\x12\x42\n\x06header\x18\x04 \x03(\x0b\x32\x32.v2ray.core.transport.internet.headers.http.Header\"&\n\x06Status\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0e\n\x06reason\x18\x02 \x01(\t\"\xde\x01\n\x0eResponseConfig\x12\x44\n\x07version\x18\x01 \x01(\x0b\x32\x33.v2ray.core.transport.internet.headers.http.Version\x12\x42\n\x06status\x18\x02 \x01(\x0b\x32\x32.v2ray.core.transport.internet.headers.http.Status\x12\x42\n\x06header\x18\x03 \x03(\x0b\x32\x32.v2ray.core.transport.internet.headers.http.Header\"\xa2\x01\n\x06\x43onfig\x12J\n\x07request\x18\x01 \x01(\x0b\x32\x39.v2ray.core.transport.internet.headers.http.RequestConfig\x12L\n\x08response\x18\x02 \x01(\x0b\x32:.v2ray.core.transport.internet.headers.http.ResponseConfigB\x9f\x01\n.com.v2ray.core.transport.internet.headers.httpP\x01Z>github.com/v2fly/v2ray-core/v5/transport/internet/headers/http\xaa\x02*V2Ray.Core.Transport.Internet.Headers.Httpb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transport.internet.headers.http.config_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n.com.v2ray.core.transport.internet.headers.httpP\001Z>github.com/v2fly/v2ray-core/v5/transport/internet/headers/http\252\002*V2Ray.Core.Transport.Internet.Headers.Http'
  _HEADER._serialized_start=92
  _HEADER._serialized_end=129
  _VERSION._serialized_start=131
  _VERSION._serialized_end=155
  _METHOD._serialized_start=157
  _METHOD._serialized_end=180
  _REQUESTCONFIG._serialized_start=183
  _REQUESTCONFIG._serialized_end=417
  _STATUS._serialized_start=419
  _STATUS._serialized_end=457
  _RESPONSECONFIG._serialized_start=460
  _RESPONSECONFIG._serialized_end=682
  _CONFIG._serialized_start=685
  _CONFIG._serialized_end=847
# @@protoc_insertion_point(module_scope)
