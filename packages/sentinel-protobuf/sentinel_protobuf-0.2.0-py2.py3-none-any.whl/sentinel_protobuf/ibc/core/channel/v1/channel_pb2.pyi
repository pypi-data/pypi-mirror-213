from gogoproto import gogo_pb2 as _gogo_pb2
from ibc.core.client.v1 import client_pb2 as _client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
ORDER_NONE_UNSPECIFIED: Order
ORDER_ORDERED: Order
ORDER_UNORDERED: Order
STATE_CLOSED: State
STATE_INIT: State
STATE_OPEN: State
STATE_TRYOPEN: State
STATE_UNINITIALIZED_UNSPECIFIED: State

class Acknowledgement(_message.Message):
    __slots__ = ["error", "result"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    error: str
    result: bytes
    def __init__(self, result: _Optional[bytes] = ..., error: _Optional[str] = ...) -> None: ...

class Channel(_message.Message):
    __slots__ = ["connection_hops", "counterparty", "ordering", "state", "version"]
    CONNECTION_HOPS_FIELD_NUMBER: _ClassVar[int]
    COUNTERPARTY_FIELD_NUMBER: _ClassVar[int]
    ORDERING_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    connection_hops: _containers.RepeatedScalarFieldContainer[str]
    counterparty: Counterparty
    ordering: Order
    state: State
    version: str
    def __init__(self, state: _Optional[_Union[State, str]] = ..., ordering: _Optional[_Union[Order, str]] = ..., counterparty: _Optional[_Union[Counterparty, _Mapping]] = ..., connection_hops: _Optional[_Iterable[str]] = ..., version: _Optional[str] = ...) -> None: ...

class Counterparty(_message.Message):
    __slots__ = ["channel_id", "port_id"]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    port_id: str
    def __init__(self, port_id: _Optional[str] = ..., channel_id: _Optional[str] = ...) -> None: ...

class IdentifiedChannel(_message.Message):
    __slots__ = ["channel_id", "connection_hops", "counterparty", "ordering", "port_id", "state", "version"]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_HOPS_FIELD_NUMBER: _ClassVar[int]
    COUNTERPARTY_FIELD_NUMBER: _ClassVar[int]
    ORDERING_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    connection_hops: _containers.RepeatedScalarFieldContainer[str]
    counterparty: Counterparty
    ordering: Order
    port_id: str
    state: State
    version: str
    def __init__(self, state: _Optional[_Union[State, str]] = ..., ordering: _Optional[_Union[Order, str]] = ..., counterparty: _Optional[_Union[Counterparty, _Mapping]] = ..., connection_hops: _Optional[_Iterable[str]] = ..., version: _Optional[str] = ..., port_id: _Optional[str] = ..., channel_id: _Optional[str] = ...) -> None: ...

class Packet(_message.Message):
    __slots__ = ["data", "destination_channel", "destination_port", "sequence", "source_channel", "source_port", "timeout_height", "timeout_timestamp"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_PORT_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    SOURCE_PORT_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    destination_channel: str
    destination_port: str
    sequence: int
    source_channel: str
    source_port: str
    timeout_height: _client_pb2.Height
    timeout_timestamp: int
    def __init__(self, sequence: _Optional[int] = ..., source_port: _Optional[str] = ..., source_channel: _Optional[str] = ..., destination_port: _Optional[str] = ..., destination_channel: _Optional[str] = ..., data: _Optional[bytes] = ..., timeout_height: _Optional[_Union[_client_pb2.Height, _Mapping]] = ..., timeout_timestamp: _Optional[int] = ...) -> None: ...

class PacketState(_message.Message):
    __slots__ = ["channel_id", "data", "port_id", "sequence"]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    data: bytes
    port_id: str
    sequence: int
    def __init__(self, port_id: _Optional[str] = ..., channel_id: _Optional[str] = ..., sequence: _Optional[int] = ..., data: _Optional[bytes] = ...) -> None: ...

class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Order(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
