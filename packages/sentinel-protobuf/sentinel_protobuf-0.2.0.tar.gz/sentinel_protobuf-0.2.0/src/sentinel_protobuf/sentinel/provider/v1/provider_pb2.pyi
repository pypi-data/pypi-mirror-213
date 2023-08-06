from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Provider(_message.Message):
    __slots__ = ["address", "description", "identity", "name", "website"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    WEBSITE_FIELD_NUMBER: _ClassVar[int]
    address: str
    description: str
    identity: str
    name: str
    website: str
    def __init__(self, address: _Optional[str] = ..., name: _Optional[str] = ..., identity: _Optional[str] = ..., website: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...
