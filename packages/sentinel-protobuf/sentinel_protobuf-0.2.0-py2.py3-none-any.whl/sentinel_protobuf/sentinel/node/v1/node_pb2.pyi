from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Node(_message.Message):
    __slots__ = ["address", "price", "provider", "remote_url", "status", "status_at"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    REMOTE_URL_FIELD_NUMBER: _ClassVar[int]
    STATUS_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    address: str
    price: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    provider: str
    remote_url: str
    status: _status_pb2.Status
    status_at: _timestamp_pb2.Timestamp
    def __init__(self, address: _Optional[str] = ..., provider: _Optional[str] = ..., price: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]] = ..., remote_url: _Optional[str] = ..., status: _Optional[_Union[_status_pb2.Status, str]] = ..., status_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
