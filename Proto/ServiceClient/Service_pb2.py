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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rService.proto\"?\n\x0cWriteRequest\x12\x0f\n\x07\x66ile_id\x18\x01 \x01(\t\x12\x10\n\x08\x63hunk_id\x18\x02 \x01(\x05\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\".\n\rWriteResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0c\n\x04\x66\x61il\x18\x02 \x01(\x08\"<\n\x0bReadRequest\x12\x0f\n\x07\x66ile_id\x18\x01 \x01(\t\x12\x0e\n\x06offset\x18\x02 \x01(\x03\x12\x0c\n\x04size\x18\x03 \x01(\x05\"-\n\x0cReadResponse\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\x12\x0f\n\x07success\x18\x02 \x01(\x08\x32\x66\n\x0f\x44\x61tanodeService\x12*\n\tWriteData\x12\r.WriteRequest\x1a\x0e.WriteResponse\x12\'\n\x08ReadData\x12\x0c.ReadRequest\x1a\r.ReadResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'Service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_WRITEREQUEST']._serialized_start=17
  _globals['_WRITEREQUEST']._serialized_end=80
  _globals['_WRITERESPONSE']._serialized_start=82
  _globals['_WRITERESPONSE']._serialized_end=128
  _globals['_READREQUEST']._serialized_start=130
  _globals['_READREQUEST']._serialized_end=190
  _globals['_READRESPONSE']._serialized_start=192
  _globals['_READRESPONSE']._serialized_end=237
  _globals['_DATANODESERVICE']._serialized_start=239
  _globals['_DATANODESERVICE']._serialized_end=341
# @@protoc_insertion_point(module_scope)
