from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ["deposit", "inactive_duration", "max_gigabyte_prices", "max_hourly_prices", "max_lease_hours", "max_leases", "min_gigabyte_prices", "min_hourly_prices", "min_lease_hours", "revenue_share"]
    DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    INACTIVE_DURATION_FIELD_NUMBER: _ClassVar[int]
    MAX_GIGABYTE_PRICES_FIELD_NUMBER: _ClassVar[int]
    MAX_HOURLY_PRICES_FIELD_NUMBER: _ClassVar[int]
    MAX_LEASES_FIELD_NUMBER: _ClassVar[int]
    MAX_LEASE_HOURS_FIELD_NUMBER: _ClassVar[int]
    MIN_GIGABYTE_PRICES_FIELD_NUMBER: _ClassVar[int]
    MIN_HOURLY_PRICES_FIELD_NUMBER: _ClassVar[int]
    MIN_LEASE_HOURS_FIELD_NUMBER: _ClassVar[int]
    REVENUE_SHARE_FIELD_NUMBER: _ClassVar[int]
    deposit: _coin_pb2.Coin
    inactive_duration: _duration_pb2.Duration
    max_gigabyte_prices: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    max_hourly_prices: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    max_lease_hours: int
    max_leases: int
    min_gigabyte_prices: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    min_hourly_prices: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    min_lease_hours: int
    revenue_share: str
    def __init__(self, deposit: _Optional[_Union[_coin_pb2.Coin, _Mapping]] = ..., inactive_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., max_gigabyte_prices: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]] = ..., min_gigabyte_prices: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]] = ..., max_hourly_prices: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]] = ..., min_hourly_prices: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]] = ..., max_lease_hours: _Optional[int] = ..., min_lease_hours: _Optional[int] = ..., max_leases: _Optional[int] = ..., revenue_share: _Optional[str] = ...) -> None: ...
