from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from sentinel.deposit.v1 import deposit_pb2 as _deposit_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryDepositRequest(_message.Message):
    __slots__ = ["address"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str
    def __init__(self, address: _Optional[str] = ...) -> None: ...

class QueryDepositResponse(_message.Message):
    __slots__ = ["deposit"]
    DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    deposit: _deposit_pb2.Deposit
    def __init__(self, deposit: _Optional[_Union[_deposit_pb2.Deposit, _Mapping]] = ...) -> None: ...

class QueryDepositsRequest(_message.Message):
    __slots__ = ["pagination"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest
    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryDepositsResponse(_message.Message):
    __slots__ = ["deposits", "pagination"]
    DEPOSITS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    deposits: _containers.RepeatedCompositeFieldContainer[_deposit_pb2.Deposit]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, deposits: _Optional[_Iterable[_Union[_deposit_pb2.Deposit, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...
