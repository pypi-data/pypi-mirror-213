from gogoproto import gogo_pb2 as _gogo_pb2
from tendermint.types import types_pb2 as _types_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CanonicalBlockID(_message.Message):
    __slots__ = ["hash", "part_set_header"]
    HASH_FIELD_NUMBER: _ClassVar[int]
    PART_SET_HEADER_FIELD_NUMBER: _ClassVar[int]
    hash: bytes
    part_set_header: CanonicalPartSetHeader
    def __init__(self, hash: _Optional[bytes] = ..., part_set_header: _Optional[_Union[CanonicalPartSetHeader, _Mapping]] = ...) -> None: ...

class CanonicalPartSetHeader(_message.Message):
    __slots__ = ["hash", "total"]
    HASH_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    hash: bytes
    total: int
    def __init__(self, total: _Optional[int] = ..., hash: _Optional[bytes] = ...) -> None: ...

class CanonicalProposal(_message.Message):
    __slots__ = ["block_id", "chain_id", "height", "pol_round", "round", "timestamp", "type"]
    BLOCK_ID_FIELD_NUMBER: _ClassVar[int]
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    POL_ROUND_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    block_id: CanonicalBlockID
    chain_id: str
    height: int
    pol_round: int
    round: int
    timestamp: _timestamp_pb2.Timestamp
    type: _types_pb2.SignedMsgType
    def __init__(self, type: _Optional[_Union[_types_pb2.SignedMsgType, str]] = ..., height: _Optional[int] = ..., round: _Optional[int] = ..., pol_round: _Optional[int] = ..., block_id: _Optional[_Union[CanonicalBlockID, _Mapping]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., chain_id: _Optional[str] = ...) -> None: ...

class CanonicalVote(_message.Message):
    __slots__ = ["block_id", "chain_id", "height", "round", "timestamp", "type"]
    BLOCK_ID_FIELD_NUMBER: _ClassVar[int]
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    block_id: CanonicalBlockID
    chain_id: str
    height: int
    round: int
    timestamp: _timestamp_pb2.Timestamp
    type: _types_pb2.SignedMsgType
    def __init__(self, type: _Optional[_Union[_types_pb2.SignedMsgType, str]] = ..., height: _Optional[int] = ..., round: _Optional[int] = ..., block_id: _Optional[_Union[CanonicalBlockID, _Mapping]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., chain_id: _Optional[str] = ...) -> None: ...
