from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from sentinel.plan.v2 import plan_pb2 as _plan_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryPlanRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class QueryPlanResponse(_message.Message):
    __slots__ = ["plan"]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    plan: _plan_pb2.Plan
    def __init__(self, plan: _Optional[_Union[_plan_pb2.Plan, _Mapping]] = ...) -> None: ...

class QueryPlansForProviderRequest(_message.Message):
    __slots__ = ["address", "pagination", "status"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    address: str
    pagination: _pagination_pb2.PageRequest
    status: _status_pb2.Status
    def __init__(self, address: _Optional[str] = ..., status: _Optional[_Union[_status_pb2.Status, str]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryPlansForProviderResponse(_message.Message):
    __slots__ = ["pagination", "plans"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    PLANS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageResponse
    plans: _containers.RepeatedCompositeFieldContainer[_plan_pb2.Plan]
    def __init__(self, plans: _Optional[_Iterable[_Union[_plan_pb2.Plan, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryPlansRequest(_message.Message):
    __slots__ = ["pagination", "status"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest
    status: _status_pb2.Status
    def __init__(self, status: _Optional[_Union[_status_pb2.Status, str]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryPlansResponse(_message.Message):
    __slots__ = ["pagination", "plans"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    PLANS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageResponse
    plans: _containers.RepeatedCompositeFieldContainer[_plan_pb2.Plan]
    def __init__(self, plans: _Optional[_Iterable[_Union[_plan_pb2.Plan, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...
