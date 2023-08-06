from gogoproto import gogo_pb2 as _gogo_pb2
from sentinel.deposit.v1 import deposit_pb2 as _deposit_pb2
from sentinel.node.v2 import genesis_pb2 as _genesis_pb2
from sentinel.plan.v2 import genesis_pb2 as _genesis_pb2_1
from sentinel.provider.v2 import genesis_pb2 as _genesis_pb2_1_1
from sentinel.session.v2 import genesis_pb2 as _genesis_pb2_1_1_1
from sentinel.subscription.v2 import genesis_pb2 as _genesis_pb2_1_1_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ["deposits", "nodes", "plans", "providers", "sessions", "subscriptions"]
    DEPOSITS_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    PLANS_FIELD_NUMBER: _ClassVar[int]
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    SESSIONS_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    deposits: _containers.RepeatedCompositeFieldContainer[_deposit_pb2.Deposit]
    nodes: _genesis_pb2.GenesisState
    plans: _containers.RepeatedCompositeFieldContainer[_genesis_pb2_1.GenesisPlan]
    providers: _genesis_pb2_1_1.GenesisState
    sessions: _genesis_pb2_1_1_1.GenesisState
    subscriptions: _genesis_pb2_1_1_1_1.GenesisState
    def __init__(self, deposits: _Optional[_Iterable[_Union[_deposit_pb2.Deposit, _Mapping]]] = ..., nodes: _Optional[_Union[_genesis_pb2.GenesisState, _Mapping]] = ..., plans: _Optional[_Iterable[_Union[_genesis_pb2_1.GenesisPlan, _Mapping]]] = ..., providers: _Optional[_Union[_genesis_pb2_1_1.GenesisState, _Mapping]] = ..., sessions: _Optional[_Union[_genesis_pb2_1_1_1.GenesisState, _Mapping]] = ..., subscriptions: _Optional[_Union[_genesis_pb2_1_1_1_1.GenesisState, _Mapping]] = ...) -> None: ...
