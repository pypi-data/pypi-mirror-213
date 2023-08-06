from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import any_pb2 as _any_pb2
from cosmos.upgrade.v1beta1 import upgrade_pb2 as _upgrade_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientConsensusStates(_message.Message):
    __slots__ = ["client_id", "consensus_states"]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CONSENSUS_STATES_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    consensus_states: _containers.RepeatedCompositeFieldContainer[ConsensusStateWithHeight]
    def __init__(self, client_id: _Optional[str] = ..., consensus_states: _Optional[_Iterable[_Union[ConsensusStateWithHeight, _Mapping]]] = ...) -> None: ...

class ClientUpdateProposal(_message.Message):
    __slots__ = ["description", "subject_client_id", "substitute_client_id", "title"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBSTITUTE_CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    description: str
    subject_client_id: str
    substitute_client_id: str
    title: str
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., subject_client_id: _Optional[str] = ..., substitute_client_id: _Optional[str] = ...) -> None: ...

class ConsensusStateWithHeight(_message.Message):
    __slots__ = ["consensus_state", "height"]
    CONSENSUS_STATE_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    consensus_state: _any_pb2.Any
    height: Height
    def __init__(self, height: _Optional[_Union[Height, _Mapping]] = ..., consensus_state: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class Height(_message.Message):
    __slots__ = ["revision_height", "revision_number"]
    REVISION_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    REVISION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    revision_height: int
    revision_number: int
    def __init__(self, revision_number: _Optional[int] = ..., revision_height: _Optional[int] = ...) -> None: ...

class IdentifiedClientState(_message.Message):
    __slots__ = ["client_id", "client_state"]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_STATE_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_state: _any_pb2.Any
    def __init__(self, client_id: _Optional[str] = ..., client_state: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class Params(_message.Message):
    __slots__ = ["allowed_clients"]
    ALLOWED_CLIENTS_FIELD_NUMBER: _ClassVar[int]
    allowed_clients: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, allowed_clients: _Optional[_Iterable[str]] = ...) -> None: ...

class UpgradeProposal(_message.Message):
    __slots__ = ["description", "plan", "title", "upgraded_client_state"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    UPGRADED_CLIENT_STATE_FIELD_NUMBER: _ClassVar[int]
    description: str
    plan: _upgrade_pb2.Plan
    title: str
    upgraded_client_state: _any_pb2.Any
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., plan: _Optional[_Union[_upgrade_pb2.Plan, _Mapping]] = ..., upgraded_client_state: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...
