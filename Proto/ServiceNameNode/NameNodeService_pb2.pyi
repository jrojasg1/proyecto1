from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class WriteBlockRequest(_message.Message):
    __slots__ = ("block_id", "chunk_index", "data")
    BLOCK_ID_FIELD_NUMBER: _ClassVar[int]
    CHUNK_INDEX_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    block_id: int
    chunk_index: int
    data: bytes
    def __init__(self, block_id: _Optional[int] = ..., chunk_index: _Optional[int] = ..., data: _Optional[bytes] = ...) -> None: ...

class WriteBlockResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class GetBlockLocationsRequest(_message.Message):
    __slots__ = ("block_id",)
    BLOCK_ID_FIELD_NUMBER: _ClassVar[int]
    block_id: int
    def __init__(self, block_id: _Optional[int] = ...) -> None: ...

class GetBlockLocationsResponse(_message.Message):
    __slots__ = ("datanodes",)
    DATANODES_FIELD_NUMBER: _ClassVar[int]
    datanodes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, datanodes: _Optional[_Iterable[str]] = ...) -> None: ...
