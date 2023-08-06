from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgRegisterRequest(_message.Message):
    __slots__ = ["gigabyte_prices", "hourly_prices", "remote_url"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    GIGABYTE_PRICES_FIELD_NUMBER: _ClassVar[int]
    HOURLY_PRICES_FIELD_NUMBER: _ClassVar[int]
    REMOTE_URL_FIELD_NUMBER: _ClassVar[int]
    gigabyte_prices: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    hourly_prices: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    remote_url: str
    def __init__(self, gigabyte_prices: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]] = ..., hourly_prices: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]] = ..., remote_url: _Optional[str] = ..., **kwargs) -> None: ...

class MsgRegisterResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MsgSubscribeRequest(_message.Message):
    __slots__ = ["address", "denom", "hours"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DENOM_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    HOURS_FIELD_NUMBER: _ClassVar[int]
    address: str
    denom: str
    hours: int
    def __init__(self, address: _Optional[str] = ..., hours: _Optional[int] = ..., denom: _Optional[str] = ..., **kwargs) -> None: ...

class MsgSubscribeResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MsgUpdateDetailsRequest(_message.Message):
    __slots__ = ["gigabyte_prices", "hourly_prices", "remote_url"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    GIGABYTE_PRICES_FIELD_NUMBER: _ClassVar[int]
    HOURLY_PRICES_FIELD_NUMBER: _ClassVar[int]
    REMOTE_URL_FIELD_NUMBER: _ClassVar[int]
    gigabyte_prices: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    hourly_prices: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    remote_url: str
    def __init__(self, gigabyte_prices: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]] = ..., hourly_prices: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]] = ..., remote_url: _Optional[str] = ..., **kwargs) -> None: ...

class MsgUpdateDetailsResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MsgUpdateStatusRequest(_message.Message):
    __slots__ = ["status"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _status_pb2.Status
    def __init__(self, status: _Optional[_Union[_status_pb2.Status, str]] = ..., **kwargs) -> None: ...

class MsgUpdateStatusResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
