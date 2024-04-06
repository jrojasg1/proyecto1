from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Block(_message.Message):
    __slots__ = ("block_id", "data")
    BLOCK_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    block_id: int
    data: bytes
    def __init__(self, block_id: _Optional[int] = ..., data: _Optional[bytes] = ...) -> None: ...

class BlockLocation(_message.Message):
    __slots__ = ("block_id", "datanodes")
    BLOCK_ID_FIELD_NUMBER: _ClassVar[int]
    DATANODES_FIELD_NUMBER: _ClassVar[int]
    block_id: int
    datanodes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, block_id: _Optional[int] = ..., datanodes: _Optional[_Iterable[str]] = ...) -> None: ...

class GetBlockLocationsRequest(_message.Message):
    __slots__ = ("block_id",)
    BLOCK_ID_FIELD_NUMBER: _ClassVar[int]
    block_id: int
    def __init__(self, block_id: _Optional[int] = ...) -> None: ...

class GetBlockLocationsResponse(_message.Message):
    __slots__ = ("block_locations",)
    BLOCK_LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    block_locations: _containers.RepeatedCompositeFieldContainer[BlockLocation]
    def __init__(self, block_locations: _Optional[_Iterable[_Union[BlockLocation, _Mapping]]] = ...) -> None: ...
