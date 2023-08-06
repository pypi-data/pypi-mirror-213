from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EventAdd(_message.Message):
    __slots__ = ["address", "coins"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    COINS_FIELD_NUMBER: _ClassVar[int]
    address: str
    coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    def __init__(self, address: _Optional[str] = ..., coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]] = ...) -> None: ...

class EventSubtract(_message.Message):
    __slots__ = ["address", "coins"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    COINS_FIELD_NUMBER: _ClassVar[int]
    address: str
    coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    def __init__(self, address: _Optional[str] = ..., coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]] = ...) -> None: ...
