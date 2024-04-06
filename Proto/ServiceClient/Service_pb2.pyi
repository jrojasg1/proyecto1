from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class WriteRequest(_message.Message):
    __slots__ = ("file_id", "data")
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    data: bytes
    def __init__(self, file_id: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class WriteResponse(_message.Message):
    __slots__ = ("success", "fail")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FAIL_FIELD_NUMBER: _ClassVar[int]
    success: bool
    fail: bool
    def __init__(self, success: bool = ..., fail: bool = ...) -> None: ...

class ReadRequest(_message.Message):
    __slots__ = ("file_id", "offset", "size")
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    offset: int
    size: int
    def __init__(self, file_id: _Optional[str] = ..., offset: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...

class ReadResponse(_message.Message):
    __slots__ = ("data", "success")
    DATA_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    success: bool
    def __init__(self, data: _Optional[bytes] = ..., success: bool = ...) -> None: ...
