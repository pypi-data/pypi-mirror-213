from gogoproto import gogo_pb2 as _gogo_pb2
from tendermint.crypto import keys_pb2 as _keys_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SimpleValidator(_message.Message):
    __slots__ = ["pub_key", "voting_power"]
    PUB_KEY_FIELD_NUMBER: _ClassVar[int]
    VOTING_POWER_FIELD_NUMBER: _ClassVar[int]
    pub_key: _keys_pb2.PublicKey
    voting_power: int
    def __init__(self, pub_key: _Optional[_Union[_keys_pb2.PublicKey, _Mapping]] = ..., voting_power: _Optional[int] = ...) -> None: ...

class Validator(_message.Message):
    __slots__ = ["address", "proposer_priority", "pub_key", "voting_power"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PROPOSER_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    PUB_KEY_FIELD_NUMBER: _ClassVar[int]
    VOTING_POWER_FIELD_NUMBER: _ClassVar[int]
    address: bytes
    proposer_priority: int
    pub_key: _keys_pb2.PublicKey
    voting_power: int
    def __init__(self, address: _Optional[bytes] = ..., pub_key: _Optional[_Union[_keys_pb2.PublicKey, _Mapping]] = ..., voting_power: _Optional[int] = ..., proposer_priority: _Optional[int] = ...) -> None: ...

class ValidatorSet(_message.Message):
    __slots__ = ["proposer", "total_voting_power", "validators"]
    PROPOSER_FIELD_NUMBER: _ClassVar[int]
    TOTAL_VOTING_POWER_FIELD_NUMBER: _ClassVar[int]
    VALIDATORS_FIELD_NUMBER: _ClassVar[int]
    proposer: Validator
    total_voting_power: int
    validators: _containers.RepeatedCompositeFieldContainer[Validator]
    def __init__(self, validators: _Optional[_Iterable[_Union[Validator, _Mapping]]] = ..., proposer: _Optional[_Union[Validator, _Mapping]] = ..., total_voting_power: _Optional[int] = ...) -> None: ...
