from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ["approve_by", "swap_denom", "swap_enabled"]
    APPROVE_BY_FIELD_NUMBER: _ClassVar[int]
    SWAP_DENOM_FIELD_NUMBER: _ClassVar[int]
    SWAP_ENABLED_FIELD_NUMBER: _ClassVar[int]
    approve_by: str
    swap_denom: str
    swap_enabled: bool
    def __init__(self, swap_enabled: bool = ..., swap_denom: _Optional[str] = ..., approve_by: _Optional[str] = ...) -> None: ...
