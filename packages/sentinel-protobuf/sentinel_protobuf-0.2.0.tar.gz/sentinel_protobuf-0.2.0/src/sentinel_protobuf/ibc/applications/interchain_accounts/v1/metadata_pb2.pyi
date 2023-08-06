from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Metadata(_message.Message):
    __slots__ = ["address", "controller_connection_id", "encoding", "host_connection_id", "tx_type", "version"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CONTROLLER_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    ENCODING_FIELD_NUMBER: _ClassVar[int]
    HOST_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    TX_TYPE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    address: str
    controller_connection_id: str
    encoding: str
    host_connection_id: str
    tx_type: str
    version: str
    def __init__(self, version: _Optional[str] = ..., controller_connection_id: _Optional[str] = ..., host_connection_id: _Optional[str] = ..., address: _Optional[str] = ..., encoding: _Optional[str] = ..., tx_type: _Optional[str] = ...) -> None: ...
