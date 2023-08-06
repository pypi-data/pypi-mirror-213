from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from sentinel.node.v2 import lease_pb2 as _lease_pb2
from sentinel.node.v2 import node_pb2 as _node_pb2
from sentinel.node.v2 import params_pb2 as _params_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryLeaseRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class QueryLeaseResponse(_message.Message):
    __slots__ = ["lease"]
    LEASE_FIELD_NUMBER: _ClassVar[int]
    lease: _lease_pb2.Lease
    def __init__(self, lease: _Optional[_Union[_lease_pb2.Lease, _Mapping]] = ...) -> None: ...

class QueryLeasesForAccountRequest(_message.Message):
    __slots__ = ["address", "pagination"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    address: str
    pagination: _pagination_pb2.PageRequest
    def __init__(self, address: _Optional[str] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryLeasesForAccountResponse(_message.Message):
    __slots__ = ["leases", "pagination"]
    LEASES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    leases: _containers.RepeatedCompositeFieldContainer[_lease_pb2.Lease]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, leases: _Optional[_Iterable[_Union[_lease_pb2.Lease, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryLeasesForNodeRequest(_message.Message):
    __slots__ = ["address", "pagination"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    address: str
    pagination: _pagination_pb2.PageRequest
    def __init__(self, address: _Optional[str] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryLeasesForNodeResponse(_message.Message):
    __slots__ = ["leases", "pagination"]
    LEASES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    leases: _containers.RepeatedCompositeFieldContainer[_lease_pb2.Lease]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, leases: _Optional[_Iterable[_Union[_lease_pb2.Lease, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryLeasesRequest(_message.Message):
    __slots__ = ["pagination"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest
    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryLeasesResponse(_message.Message):
    __slots__ = ["leases", "pagination"]
    LEASES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    leases: _containers.RepeatedCompositeFieldContainer[_lease_pb2.Lease]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, leases: _Optional[_Iterable[_Union[_lease_pb2.Lease, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryNodeRequest(_message.Message):
    __slots__ = ["address"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str
    def __init__(self, address: _Optional[str] = ...) -> None: ...

class QueryNodeResponse(_message.Message):
    __slots__ = ["node"]
    NODE_FIELD_NUMBER: _ClassVar[int]
    node: _node_pb2.Node
    def __init__(self, node: _Optional[_Union[_node_pb2.Node, _Mapping]] = ...) -> None: ...

class QueryNodesForPlanRequest(_message.Message):
    __slots__ = ["id", "pagination", "status"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: int
    pagination: _pagination_pb2.PageRequest
    status: _status_pb2.Status
    def __init__(self, id: _Optional[int] = ..., status: _Optional[_Union[_status_pb2.Status, str]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryNodesForPlanResponse(_message.Message):
    __slots__ = ["nodes", "pagination"]
    NODES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[_node_pb2.Node]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, nodes: _Optional[_Iterable[_Union[_node_pb2.Node, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryNodesRequest(_message.Message):
    __slots__ = ["pagination", "status"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest
    status: _status_pb2.Status
    def __init__(self, status: _Optional[_Union[_status_pb2.Status, str]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryNodesResponse(_message.Message):
    __slots__ = ["nodes", "pagination"]
    NODES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[_node_pb2.Node]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, nodes: _Optional[_Iterable[_Union[_node_pb2.Node, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryParamsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class QueryParamsResponse(_message.Message):
    __slots__ = ["params"]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params
    def __init__(self, params: _Optional[_Union[_params_pb2.Params, _Mapping]] = ...) -> None: ...
