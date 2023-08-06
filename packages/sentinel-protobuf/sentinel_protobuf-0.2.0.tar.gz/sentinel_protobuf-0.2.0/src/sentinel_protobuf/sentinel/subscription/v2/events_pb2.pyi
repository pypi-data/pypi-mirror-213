from gogoproto import gogo_pb2 as _gogo_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EventAddQuota(_message.Message):
    __slots__ = ["address", "id"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    id: int
    def __init__(self, id: _Optional[int] = ..., address: _Optional[str] = ...) -> None: ...

class EventSetStatus(_message.Message):
    __slots__ = ["id", "status"]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: int
    status: _status_pb2.Status
    def __init__(self, id: _Optional[int] = ..., status: _Optional[_Union[_status_pb2.Status, str]] = ...) -> None: ...

class EventSubscribe(_message.Message):
    __slots__ = ["id", "node", "plan"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    id: int
    node: str
    plan: int
    def __init__(self, id: _Optional[int] = ..., node: _Optional[str] = ..., plan: _Optional[int] = ...) -> None: ...

class EventUpdateQuota(_message.Message):
    __slots__ = ["address", "id"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    id: int
    def __init__(self, id: _Optional[int] = ..., address: _Optional[str] = ...) -> None: ...
