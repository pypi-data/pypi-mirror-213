from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from sentinel.session.v2 import session_pb2 as _session_pb2
from sentinel.session.v2 import params_pb2 as _params_pb2
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

class QuerySessionRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class QuerySessionResponse(_message.Message):
    __slots__ = ["session"]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    session: _session_pb2.Session
    def __init__(self, session: _Optional[_Union[_session_pb2.Session, _Mapping]] = ...) -> None: ...

class QuerySessionsForAccountRequest(_message.Message):
    __slots__ = ["address", "pagination"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    address: str
    pagination: _pagination_pb2.PageRequest
    def __init__(self, address: _Optional[str] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QuerySessionsForAccountResponse(_message.Message):
    __slots__ = ["pagination", "sessions"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SESSIONS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageResponse
    sessions: _containers.RepeatedCompositeFieldContainer[_session_pb2.Session]
    def __init__(self, sessions: _Optional[_Iterable[_Union[_session_pb2.Session, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QuerySessionsForNodeRequest(_message.Message):
    __slots__ = ["address", "pagination"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    address: str
    pagination: _pagination_pb2.PageRequest
    def __init__(self, address: _Optional[str] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QuerySessionsForNodeResponse(_message.Message):
    __slots__ = ["pagination", "sessions"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SESSIONS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageResponse
    sessions: _containers.RepeatedCompositeFieldContainer[_session_pb2.Session]
    def __init__(self, sessions: _Optional[_Iterable[_Union[_session_pb2.Session, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QuerySessionsForSubscriptionRequest(_message.Message):
    __slots__ = ["id", "pagination"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    id: int
    pagination: _pagination_pb2.PageRequest
    def __init__(self, id: _Optional[int] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QuerySessionsForSubscriptionResponse(_message.Message):
    __slots__ = ["pagination", "sessions"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SESSIONS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageResponse
    sessions: _containers.RepeatedCompositeFieldContainer[_session_pb2.Session]
    def __init__(self, sessions: _Optional[_Iterable[_Union[_session_pb2.Session, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QuerySessionsRequest(_message.Message):
    __slots__ = ["pagination"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest
    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QuerySessionsResponse(_message.Message):
    __slots__ = ["pagination", "sessions"]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SESSIONS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageResponse
    sessions: _containers.RepeatedCompositeFieldContainer[_session_pb2.Session]
    def __init__(self, sessions: _Optional[_Iterable[_Union[_session_pb2.Session, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...
