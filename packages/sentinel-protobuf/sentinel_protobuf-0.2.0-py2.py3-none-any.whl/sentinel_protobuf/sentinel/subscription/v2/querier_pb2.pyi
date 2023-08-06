from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import any_pb2 as _any_pb2
from sentinel.subscription.v2 import params_pb2 as _params_pb2
from sentinel.subscription.v2 import quota_pb2 as _quota_pb2
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

class QueryQuotaRequest(_message.Message):
    __slots__ = ["address", "id"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    id: int
    def __init__(self, id: _Optional[int] = ..., address: _Optional[str] = ...) -> None: ...

class QueryQuotaResponse(_message.Message):
    __slots__ = ["quota"]
    QUOTA_FIELD_NUMBER: _ClassVar[int]
    quota: _quota_pb2.Quota
    def __init__(self, quota: _Optional[_Union[_quota_pb2.Quota, _Mapping]] = ...) -> None: ...

class QueryQuotasRequest(_message.Message):
    __slots__ = ["id", "pagination"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    id: int
    pagination: _pagination_pb2.PageRequest
    def __init__(self, id: _Optional[int] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryQuotasResponse(_message.Message):
    __slots__ = ["pagination", "quotas"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    QUOTAS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageResponse
    quotas: _containers.RepeatedCompositeFieldContainer[_quota_pb2.Quota]
    def __init__(self, quotas: _Optional[_Iterable[_Union[_quota_pb2.Quota, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QuerySubscriptionRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class QuerySubscriptionResponse(_message.Message):
    __slots__ = ["subscription"]
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    subscription: _any_pb2.Any
    def __init__(self, subscription: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class QuerySubscriptionsForAccountRequest(_message.Message):
    __slots__ = ["address", "pagination"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    address: str
    pagination: _pagination_pb2.PageRequest
    def __init__(self, address: _Optional[str] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QuerySubscriptionsForAccountResponse(_message.Message):
    __slots__ = ["pagination", "subscriptions"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageResponse
    subscriptions: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, subscriptions: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QuerySubscriptionsForNodeRequest(_message.Message):
    __slots__ = ["address", "pagination"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    address: str
    pagination: _pagination_pb2.PageRequest
    def __init__(self, address: _Optional[str] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QuerySubscriptionsForNodeResponse(_message.Message):
    __slots__ = ["pagination", "subscriptions"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageResponse
    subscriptions: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, subscriptions: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QuerySubscriptionsForPlanRequest(_message.Message):
    __slots__ = ["id", "pagination"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    id: int
    pagination: _pagination_pb2.PageRequest
    def __init__(self, id: _Optional[int] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QuerySubscriptionsForPlanResponse(_message.Message):
    __slots__ = ["pagination", "subscriptions"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageResponse
    subscriptions: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, subscriptions: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QuerySubscriptionsRequest(_message.Message):
    __slots__ = ["pagination"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest
    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QuerySubscriptionsResponse(_message.Message):
    __slots__ = ["pagination", "subscriptions"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageResponse
    subscriptions: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, subscriptions: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...
