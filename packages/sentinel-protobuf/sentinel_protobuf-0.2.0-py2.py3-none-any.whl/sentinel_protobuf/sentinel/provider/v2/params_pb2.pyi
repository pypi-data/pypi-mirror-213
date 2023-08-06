from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ["deposit", "revenue_share"]
    DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    REVENUE_SHARE_FIELD_NUMBER: _ClassVar[int]
    deposit: _coin_pb2.Coin
    revenue_share: str
    def __init__(self, deposit: _Optional[_Union[_coin_pb2.Coin, _Mapping]] = ..., revenue_share: _Optional[str] = ...) -> None: ...
