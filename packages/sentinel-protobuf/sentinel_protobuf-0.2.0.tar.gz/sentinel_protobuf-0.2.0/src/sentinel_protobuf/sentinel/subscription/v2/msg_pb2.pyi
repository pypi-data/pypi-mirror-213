from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MsgCancelRequest(_message.Message):
    __slots__ = ["id"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ..., **kwargs) -> None: ...

class MsgCancelResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MsgShareRequest(_message.Message):
    __slots__ = ["address", "bytes", "id"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    bytes: str
    id: int
    def __init__(self, id: _Optional[int] = ..., address: _Optional[str] = ..., bytes: _Optional[str] = ..., **kwargs) -> None: ...

class MsgShareResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MsgUpdateQuotaRequest(_message.Message):
    __slots__ = ["address", "bytes", "id"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    bytes: str
    id: int
    def __init__(self, id: _Optional[int] = ..., address: _Optional[str] = ..., bytes: _Optional[str] = ..., **kwargs) -> None: ...

class MsgUpdateQuotaResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
