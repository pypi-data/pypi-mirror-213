from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Plan(_message.Message):
    __slots__ = ["bytes", "id", "price", "provider", "status", "status_at", "validity"]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    STATUS_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VALIDITY_FIELD_NUMBER: _ClassVar[int]
    bytes: str
    id: int
    price: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    provider: str
    status: _status_pb2.Status
    status_at: _timestamp_pb2.Timestamp
    validity: _duration_pb2.Duration
    def __init__(self, id: _Optional[int] = ..., provider: _Optional[str] = ..., price: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]] = ..., validity: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., bytes: _Optional[str] = ..., status: _Optional[_Union[_status_pb2.Status, str]] = ..., status_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
