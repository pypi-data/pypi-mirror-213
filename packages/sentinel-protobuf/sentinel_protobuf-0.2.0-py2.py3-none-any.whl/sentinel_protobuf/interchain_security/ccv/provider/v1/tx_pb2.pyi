from google.api import annotations_pb2 as _annotations_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgAssignConsumerKey(_message.Message):
    __slots__ = ["chain_id", "consumer_key", "provider_addr"]
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_KEY_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_ADDR_FIELD_NUMBER: _ClassVar[int]
    chain_id: str
    consumer_key: _any_pb2.Any
    provider_addr: str
    def __init__(self, chain_id: _Optional[str] = ..., provider_addr: _Optional[str] = ..., consumer_key: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class MsgAssignConsumerKeyResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
