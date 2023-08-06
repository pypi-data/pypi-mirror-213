from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DenomTrace(_message.Message):
    __slots__ = ["base_denom", "path"]
    BASE_DENOM_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    base_denom: str
    path: str
    def __init__(self, path: _Optional[str] = ..., base_denom: _Optional[str] = ...) -> None: ...

class Params(_message.Message):
    __slots__ = ["receive_enabled", "send_enabled"]
    RECEIVE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SEND_ENABLED_FIELD_NUMBER: _ClassVar[int]
    receive_enabled: bool
    send_enabled: bool
    def __init__(self, send_enabled: bool = ..., receive_enabled: bool = ...) -> None: ...
