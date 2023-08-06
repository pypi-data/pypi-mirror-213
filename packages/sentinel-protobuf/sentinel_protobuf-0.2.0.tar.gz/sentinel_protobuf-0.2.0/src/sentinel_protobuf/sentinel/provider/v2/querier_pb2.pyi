from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from sentinel.provider.v2 import params_pb2 as _params_pb2
from sentinel.provider.v2 import provider_pb2 as _provider_pb2
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

class QueryProviderRequest(_message.Message):
    __slots__ = ["address"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str
    def __init__(self, address: _Optional[str] = ...) -> None: ...

class QueryProviderResponse(_message.Message):
    __slots__ = ["provider"]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    provider: _provider_pb2.Provider
    def __init__(self, provider: _Optional[_Union[_provider_pb2.Provider, _Mapping]] = ...) -> None: ...

class QueryProvidersRequest(_message.Message):
    __slots__ = ["pagination", "status"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest
    status: _status_pb2.Status
    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ..., status: _Optional[_Union[_status_pb2.Status, str]] = ...) -> None: ...

class QueryProvidersResponse(_message.Message):
    __slots__ = ["pagination", "providers"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageResponse
    providers: _containers.RepeatedCompositeFieldContainer[_provider_pb2.Provider]
    def __init__(self, providers: _Optional[_Iterable[_Union[_provider_pb2.Provider, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...
