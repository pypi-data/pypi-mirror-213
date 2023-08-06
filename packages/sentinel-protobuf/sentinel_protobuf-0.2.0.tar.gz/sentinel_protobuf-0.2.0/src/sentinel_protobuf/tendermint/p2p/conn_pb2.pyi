from gogoproto import gogo_pb2 as _gogo_pb2
from tendermint.crypto import keys_pb2 as _keys_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuthSigMessage(_message.Message):
    __slots__ = ["pub_key", "sig"]
    PUB_KEY_FIELD_NUMBER: _ClassVar[int]
    SIG_FIELD_NUMBER: _ClassVar[int]
    pub_key: _keys_pb2.PublicKey
    sig: bytes
    def __init__(self, pub_key: _Optional[_Union[_keys_pb2.PublicKey, _Mapping]] = ..., sig: _Optional[bytes] = ...) -> None: ...

class Packet(_message.Message):
    __slots__ = ["packet_msg", "packet_ping", "packet_pong"]
    PACKET_MSG_FIELD_NUMBER: _ClassVar[int]
    PACKET_PING_FIELD_NUMBER: _ClassVar[int]
    PACKET_PONG_FIELD_NUMBER: _ClassVar[int]
    packet_msg: PacketMsg
    packet_ping: PacketPing
    packet_pong: PacketPong
    def __init__(self, packet_ping: _Optional[_Union[PacketPing, _Mapping]] = ..., packet_pong: _Optional[_Union[PacketPong, _Mapping]] = ..., packet_msg: _Optional[_Union[PacketMsg, _Mapping]] = ...) -> None: ...

class PacketMsg(_message.Message):
    __slots__ = ["channel_id", "data", "eof"]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    EOF_FIELD_NUMBER: _ClassVar[int]
    channel_id: int
    data: bytes
    eof: bool
    def __init__(self, channel_id: _Optional[int] = ..., eof: bool = ..., data: _Optional[bytes] = ...) -> None: ...

class PacketPing(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PacketPong(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
