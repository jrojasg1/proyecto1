# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: NameNodeService.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15NameNodeService.proto\"H\n\x11WriteBlockRequest\x12\x10\n\x08\x62lock_id\x18\x01 \x01(\x05\x12\x13\n\x0b\x63hunk_index\x18\x02 \x01(\x05\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\"%\n\x12WriteBlockResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\",\n\x18GetBlockLocationsRequest\x12\x10\n\x08\x62lock_id\x18\x01 \x01(\x05\".\n\x19GetBlockLocationsResponse\x12\x11\n\tdatanodes\x18\x01 \x03(\tb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'NameNodeService_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_WRITEBLOCKREQUEST']._serialized_start=25
  _globals['_WRITEBLOCKREQUEST']._serialized_end=97
  _globals['_WRITEBLOCKRESPONSE']._serialized_start=99
  _globals['_WRITEBLOCKRESPONSE']._serialized_end=136
  _globals['_GETBLOCKLOCATIONSREQUEST']._serialized_start=138
  _globals['_GETBLOCKLOCATIONSREQUEST']._serialized_end=182
  _globals['_GETBLOCKLOCATIONSRESPONSE']._serialized_start=184
  _globals['_GETBLOCKLOCATIONSRESPONSE']._serialized_end=230
# @@protoc_insertion_point(module_scope)
