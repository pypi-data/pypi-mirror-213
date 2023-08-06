from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from sentinel.types.v1 import bandwidth_pb2 as _bandwidth_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Session(_message.Message):
    __slots__ = ["address", "bandwidth", "duration", "id", "node", "status", "status_at", "subscription"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    BANDWIDTH_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    STATUS_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    address: str
    bandwidth: _bandwidth_pb2.Bandwidth
    duration: _duration_pb2.Duration
    id: int
    node: str
    status: _status_pb2.Status
    status_at: _timestamp_pb2.Timestamp
    subscription: int
    def __init__(self, id: _Optional[int] = ..., subscription: _Optional[int] = ..., node: _Optional[str] = ..., address: _Optional[str] = ..., duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., bandwidth: _Optional[_Union[_bandwidth_pb2.Bandwidth, _Mapping]] = ..., status: _Optional[_Union[_status_pb2.Status, str]] = ..., status_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
