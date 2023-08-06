from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EventPay(_message.Message):
    __slots__ = ["amount", "id", "node", "subscription"]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    amount: _coin_pb2.Coin
    id: int
    node: str
    subscription: int
    def __init__(self, id: _Optional[int] = ..., node: _Optional[str] = ..., subscription: _Optional[int] = ..., amount: _Optional[_Union[_coin_pb2.Coin, _Mapping]] = ...) -> None: ...

class EventSetStatus(_message.Message):
    __slots__ = ["id", "node", "status", "subscription"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: int
    node: str
    status: _status_pb2.Status
    subscription: int
    def __init__(self, id: _Optional[int] = ..., node: _Optional[str] = ..., subscription: _Optional[int] = ..., status: _Optional[_Union[_status_pb2.Status, str]] = ...) -> None: ...

class EventStart(_message.Message):
    __slots__ = ["id", "node", "subscription"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: int
    node: str
    subscription: int
    def __init__(self, id: _Optional[int] = ..., node: _Optional[str] = ..., subscription: _Optional[int] = ...) -> None: ...

class EventUpdate(_message.Message):
    __slots__ = ["id", "node", "subscription"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: int
    node: str
    subscription: int
    def __init__(self, id: _Optional[int] = ..., node: _Optional[str] = ..., subscription: _Optional[int] = ...) -> None: ...
