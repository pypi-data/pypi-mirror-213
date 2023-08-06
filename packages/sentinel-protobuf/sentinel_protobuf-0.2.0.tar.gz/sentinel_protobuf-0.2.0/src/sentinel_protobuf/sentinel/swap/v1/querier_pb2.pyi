from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from sentinel.swap.v1 import swap_pb2 as _swap_pb2
from sentinel.swap.v1 import params_pb2 as _params_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryParamsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class QueryParamsResponse(_message.Message):
    __slots__ = ["params"]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params
    def __init__(self, params: _Optional[_Union[_params_pb2.Params, _Mapping]] = ...) -> None: ...

class QuerySwapRequest(_message.Message):
    __slots__ = ["tx_hash"]
    TX_HASH_FIELD_NUMBER: _ClassVar[int]
    tx_hash: bytes
    def __init__(self, tx_hash: _Optional[bytes] = ...) -> None: ...

class QuerySwapResponse(_message.Message):
    __slots__ = ["swap"]
    SWAP_FIELD_NUMBER: _ClassVar[int]
    swap: _swap_pb2.Swap
    def __init__(self, swap: _Optional[_Union[_swap_pb2.Swap, _Mapping]] = ...) -> None: ...

class QuerySwapsRequest(_message.Message):
    __slots__ = ["pagination"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest
    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QuerySwapsResponse(_message.Message):
    __slots__ = ["pagination", "swaps"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SWAPS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageResponse
    swaps: _containers.RepeatedCompositeFieldContainer[_swap_pb2.Swap]
    def __init__(self, swaps: _Optional[_Iterable[_Union[_swap_pb2.Swap, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...
