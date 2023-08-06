from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DefaultNodeInfo(_message.Message):
    __slots__ = ["channels", "default_node_id", "listen_addr", "moniker", "network", "other", "protocol_version", "version"]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    LISTEN_ADDR_FIELD_NUMBER: _ClassVar[int]
    MONIKER_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    OTHER_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    channels: bytes
    default_node_id: str
    listen_addr: str
    moniker: str
    network: str
    other: DefaultNodeInfoOther
    protocol_version: ProtocolVersion
    version: str
    def __init__(self, protocol_version: _Optional[_Union[ProtocolVersion, _Mapping]] = ..., default_node_id: _Optional[str] = ..., listen_addr: _Optional[str] = ..., network: _Optional[str] = ..., version: _Optional[str] = ..., channels: _Optional[bytes] = ..., moniker: _Optional[str] = ..., other: _Optional[_Union[DefaultNodeInfoOther, _Mapping]] = ...) -> None: ...

class DefaultNodeInfoOther(_message.Message):
    __slots__ = ["rpc_address", "tx_index"]
    RPC_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TX_INDEX_FIELD_NUMBER: _ClassVar[int]
    rpc_address: str
    tx_index: str
    def __init__(self, tx_index: _Optional[str] = ..., rpc_address: _Optional[str] = ...) -> None: ...

class NetAddress(_message.Message):
    __slots__ = ["id", "ip", "port"]
    ID_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    id: str
    ip: str
    port: int
    def __init__(self, id: _Optional[str] = ..., ip: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class ProtocolVersion(_message.Message):
    __slots__ = ["app", "block", "p2p"]
    APP_FIELD_NUMBER: _ClassVar[int]
    BLOCK_FIELD_NUMBER: _ClassVar[int]
    P2P_FIELD_NUMBER: _ClassVar[int]
    app: int
    block: int
    p2p: int
    def __init__(self, p2p: _Optional[int] = ..., block: _Optional[int] = ..., app: _Optional[int] = ...) -> None: ...
