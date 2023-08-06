from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Quota(_message.Message):
    __slots__ = ["address", "allocated", "consumed"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ALLOCATED_FIELD_NUMBER: _ClassVar[int]
    CONSUMED_FIELD_NUMBER: _ClassVar[int]
    address: str
    allocated: str
    consumed: str
    def __init__(self, address: _Optional[str] = ..., allocated: _Optional[str] = ..., consumed: _Optional[str] = ...) -> None: ...
