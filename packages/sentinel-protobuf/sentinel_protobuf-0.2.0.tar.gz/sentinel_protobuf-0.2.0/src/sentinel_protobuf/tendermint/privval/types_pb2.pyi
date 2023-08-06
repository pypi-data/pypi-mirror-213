from tendermint.crypto import keys_pb2 as _keys_pb2
from tendermint.types import types_pb2 as _types_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
ERRORS_CONNECTION_TIMEOUT: Errors
ERRORS_NO_CONNECTION: Errors
ERRORS_READ_TIMEOUT: Errors
ERRORS_UNEXPECTED_RESPONSE: Errors
ERRORS_UNKNOWN: Errors
ERRORS_WRITE_TIMEOUT: Errors

class Message(_message.Message):
    __slots__ = ["ping_request", "ping_response", "pub_key_request", "pub_key_response", "sign_proposal_request", "sign_vote_request", "signed_proposal_response", "signed_vote_response"]
    PING_REQUEST_FIELD_NUMBER: _ClassVar[int]
    PING_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    PUB_KEY_REQUEST_FIELD_NUMBER: _ClassVar[int]
    PUB_KEY_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SIGNED_PROPOSAL_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SIGNED_VOTE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SIGN_PROPOSAL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    SIGN_VOTE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    ping_request: PingRequest
    ping_response: PingResponse
    pub_key_request: PubKeyRequest
    pub_key_response: PubKeyResponse
    sign_proposal_request: SignProposalRequest
    sign_vote_request: SignVoteRequest
    signed_proposal_response: SignedProposalResponse
    signed_vote_response: SignedVoteResponse
    def __init__(self, pub_key_request: _Optional[_Union[PubKeyRequest, _Mapping]] = ..., pub_key_response: _Optional[_Union[PubKeyResponse, _Mapping]] = ..., sign_vote_request: _Optional[_Union[SignVoteRequest, _Mapping]] = ..., signed_vote_response: _Optional[_Union[SignedVoteResponse, _Mapping]] = ..., sign_proposal_request: _Optional[_Union[SignProposalRequest, _Mapping]] = ..., signed_proposal_response: _Optional[_Union[SignedProposalResponse, _Mapping]] = ..., ping_request: _Optional[_Union[PingRequest, _Mapping]] = ..., ping_response: _Optional[_Union[PingResponse, _Mapping]] = ...) -> None: ...

class PingRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PingResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PubKeyRequest(_message.Message):
    __slots__ = ["chain_id"]
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    chain_id: str
    def __init__(self, chain_id: _Optional[str] = ...) -> None: ...

class PubKeyResponse(_message.Message):
    __slots__ = ["error", "pub_key"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PUB_KEY_FIELD_NUMBER: _ClassVar[int]
    error: RemoteSignerError
    pub_key: _keys_pb2.PublicKey
    def __init__(self, pub_key: _Optional[_Union[_keys_pb2.PublicKey, _Mapping]] = ..., error: _Optional[_Union[RemoteSignerError, _Mapping]] = ...) -> None: ...

class RemoteSignerError(_message.Message):
    __slots__ = ["code", "description"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    code: int
    description: str
    def __init__(self, code: _Optional[int] = ..., description: _Optional[str] = ...) -> None: ...

class SignProposalRequest(_message.Message):
    __slots__ = ["chain_id", "proposal"]
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    chain_id: str
    proposal: _types_pb2.Proposal
    def __init__(self, proposal: _Optional[_Union[_types_pb2.Proposal, _Mapping]] = ..., chain_id: _Optional[str] = ...) -> None: ...

class SignVoteRequest(_message.Message):
    __slots__ = ["chain_id", "vote"]
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    VOTE_FIELD_NUMBER: _ClassVar[int]
    chain_id: str
    vote: _types_pb2.Vote
    def __init__(self, vote: _Optional[_Union[_types_pb2.Vote, _Mapping]] = ..., chain_id: _Optional[str] = ...) -> None: ...

class SignedProposalResponse(_message.Message):
    __slots__ = ["error", "proposal"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    error: RemoteSignerError
    proposal: _types_pb2.Proposal
    def __init__(self, proposal: _Optional[_Union[_types_pb2.Proposal, _Mapping]] = ..., error: _Optional[_Union[RemoteSignerError, _Mapping]] = ...) -> None: ...

class SignedVoteResponse(_message.Message):
    __slots__ = ["error", "vote"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    VOTE_FIELD_NUMBER: _ClassVar[int]
    error: RemoteSignerError
    vote: _types_pb2.Vote
    def __init__(self, vote: _Optional[_Union[_types_pb2.Vote, _Mapping]] = ..., error: _Optional[_Union[RemoteSignerError, _Mapping]] = ...) -> None: ...

class Errors(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
