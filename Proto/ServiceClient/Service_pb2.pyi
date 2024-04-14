from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class WriteRequest(_message.Message):
    __slots__ = ("file_id", "chunk_id", "data")
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    CHUNK_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    chunk_id: int
    data: bytes
    def __init__(self, file_id: _Optional[str] = ..., chunk_id: _Optional[int] = ..., data: _Optional[bytes] = ...) -> None: ...

class WriteResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class ReadRequest(_message.Message):
    __slots__ = ("file_id", "chunk_id", "size")
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    CHUNK_ID_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    chunk_id: int
    size: int
    def __init__(self, file_id: _Optional[str] = ..., chunk_id: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...

class ReadResponse(_message.Message):
    __slots__ = ("data", "success")
    DATA_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    success: bool
    def __init__(self, data: _Optional[bytes] = ..., success: bool = ...) -> None: ...
