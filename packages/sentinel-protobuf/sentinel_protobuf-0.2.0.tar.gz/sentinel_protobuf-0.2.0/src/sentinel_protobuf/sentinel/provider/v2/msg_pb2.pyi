from gogoproto import gogo_pb2 as _gogo_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgRegisterRequest(_message.Message):
    __slots__ = ["description", "identity", "name", "website"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    WEBSITE_FIELD_NUMBER: _ClassVar[int]
    description: str
    identity: str
    name: str
    website: str
    def __init__(self, name: _Optional[str] = ..., identity: _Optional[str] = ..., website: _Optional[str] = ..., description: _Optional[str] = ..., **kwargs) -> None: ...

class MsgRegisterResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MsgUpdateRequest(_message.Message):
    __slots__ = ["description", "identity", "name", "status", "website"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    WEBSITE_FIELD_NUMBER: _ClassVar[int]
    description: str
    identity: str
    name: str
    status: _status_pb2.Status
    website: str
    def __init__(self, name: _Optional[str] = ..., identity: _Optional[str] = ..., website: _Optional[str] = ..., description: _Optional[str] = ..., status: _Optional[_Union[_status_pb2.Status, str]] = ..., **kwargs) -> None: ...

class MsgUpdateResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
