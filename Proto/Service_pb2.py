# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Service.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rService.proto\"-\n\x0cWriteRequest\x12\x0f\n\x07\x66ile_id\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\"\x0f\n\rWriteResponse\"<\n\x0bReadRequest\x12\x0f\n\x07\x66ile_id\x18\x01 \x01(\t\x12\x0e\n\x06offset\x18\x02 \x01(\x03\x12\x0c\n\x04size\x18\x03 \x01(\x05\"\x0e\n\x0cReadResponse2f\n\x0f\x44\x61tanodeService\x12*\n\tWriteData\x12\r.WriteRequest\x1a\x0e.WriteResponse\x12\'\n\x08ReadData\x12\x0c.ReadRequest\x1a\r.ReadResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'Service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_WRITEREQUEST']._serialized_start=17
  _globals['_WRITEREQUEST']._serialized_end=62
  _globals['_WRITERESPONSE']._serialized_start=64
  _globals['_WRITERESPONSE']._serialized_end=79
  _globals['_READREQUEST']._serialized_start=81
  _globals['_READREQUEST']._serialized_end=141
  _globals['_READRESPONSE']._serialized_start=143
  _globals['_READRESPONSE']._serialized_end=157
  _globals['_DATANODESERVICE']._serialized_start=159
  _globals['_DATANODESERVICE']._serialized_end=261
# @@protoc_insertion_point(module_scope)
