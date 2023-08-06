from gogoproto import gogo_pb2 as _gogo_pb2
from tendermint.types import types_pb2 as _types_pb2
from tendermint.libs.bits import types_pb2 as _types_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BlockPart(_message.Message):
    __slots__ = ["height", "part", "round"]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    PART_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    height: int
    part: _types_pb2.Part
    round: int
    def __init__(self, height: _Optional[int] = ..., round: _Optional[int] = ..., part: _Optional[_Union[_types_pb2.Part, _Mapping]] = ...) -> None: ...

class HasVote(_message.Message):
    __slots__ = ["height", "index", "round", "type"]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    height: int
    index: int
    round: int
    type: _types_pb2.SignedMsgType
    def __init__(self, height: _Optional[int] = ..., round: _Optional[int] = ..., type: _Optional[_Union[_types_pb2.SignedMsgType, str]] = ..., index: _Optional[int] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ["block_part", "has_vote", "new_round_step", "new_valid_block", "proposal", "proposal_pol", "vote", "vote_set_bits", "vote_set_maj23"]
    BLOCK_PART_FIELD_NUMBER: _ClassVar[int]
    HAS_VOTE_FIELD_NUMBER: _ClassVar[int]
    NEW_ROUND_STEP_FIELD_NUMBER: _ClassVar[int]
    NEW_VALID_BLOCK_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_POL_FIELD_NUMBER: _ClassVar[int]
    VOTE_FIELD_NUMBER: _ClassVar[int]
    VOTE_SET_BITS_FIELD_NUMBER: _ClassVar[int]
    VOTE_SET_MAJ23_FIELD_NUMBER: _ClassVar[int]
    block_part: BlockPart
    has_vote: HasVote
    new_round_step: NewRoundStep
    new_valid_block: NewValidBlock
    proposal: Proposal
    proposal_pol: ProposalPOL
    vote: Vote
    vote_set_bits: VoteSetBits
    vote_set_maj23: VoteSetMaj23
    def __init__(self, new_round_step: _Optional[_Union[NewRoundStep, _Mapping]] = ..., new_valid_block: _Optional[_Union[NewValidBlock, _Mapping]] = ..., proposal: _Optional[_Union[Proposal, _Mapping]] = ..., proposal_pol: _Optional[_Union[ProposalPOL, _Mapping]] = ..., block_part: _Optional[_Union[BlockPart, _Mapping]] = ..., vote: _Optional[_Union[Vote, _Mapping]] = ..., has_vote: _Optional[_Union[HasVote, _Mapping]] = ..., vote_set_maj23: _Optional[_Union[VoteSetMaj23, _Mapping]] = ..., vote_set_bits: _Optional[_Union[VoteSetBits, _Mapping]] = ...) -> None: ...

class NewRoundStep(_message.Message):
    __slots__ = ["height", "last_commit_round", "round", "seconds_since_start_time", "step"]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    LAST_COMMIT_ROUND_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    SECONDS_SINCE_START_TIME_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    height: int
    last_commit_round: int
    round: int
    seconds_since_start_time: int
    step: int
    def __init__(self, height: _Optional[int] = ..., round: _Optional[int] = ..., step: _Optional[int] = ..., seconds_since_start_time: _Optional[int] = ..., last_commit_round: _Optional[int] = ...) -> None: ...

class NewValidBlock(_message.Message):
    __slots__ = ["block_part_set_header", "block_parts", "height", "is_commit", "round"]
    BLOCK_PARTS_FIELD_NUMBER: _ClassVar[int]
    BLOCK_PART_SET_HEADER_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    IS_COMMIT_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    block_part_set_header: _types_pb2.PartSetHeader
    block_parts: _types_pb2_1.BitArray
    height: int
    is_commit: bool
    round: int
    def __init__(self, height: _Optional[int] = ..., round: _Optional[int] = ..., block_part_set_header: _Optional[_Union[_types_pb2.PartSetHeader, _Mapping]] = ..., block_parts: _Optional[_Union[_types_pb2_1.BitArray, _Mapping]] = ..., is_commit: bool = ...) -> None: ...

class Proposal(_message.Message):
    __slots__ = ["proposal"]
    PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    proposal: _types_pb2.Proposal
    def __init__(self, proposal: _Optional[_Union[_types_pb2.Proposal, _Mapping]] = ...) -> None: ...

class ProposalPOL(_message.Message):
    __slots__ = ["height", "proposal_pol", "proposal_pol_round"]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_POL_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_POL_ROUND_FIELD_NUMBER: _ClassVar[int]
    height: int
    proposal_pol: _types_pb2_1.BitArray
    proposal_pol_round: int
    def __init__(self, height: _Optional[int] = ..., proposal_pol_round: _Optional[int] = ..., proposal_pol: _Optional[_Union[_types_pb2_1.BitArray, _Mapping]] = ...) -> None: ...

class Vote(_message.Message):
    __slots__ = ["vote"]
    VOTE_FIELD_NUMBER: _ClassVar[int]
    vote: _types_pb2.Vote
    def __init__(self, vote: _Optional[_Union[_types_pb2.Vote, _Mapping]] = ...) -> None: ...

class VoteSetBits(_message.Message):
    __slots__ = ["block_id", "height", "round", "type", "votes"]
    BLOCK_ID_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VOTES_FIELD_NUMBER: _ClassVar[int]
    block_id: _types_pb2.BlockID
    height: int
    round: int
    type: _types_pb2.SignedMsgType
    votes: _types_pb2_1.BitArray
    def __init__(self, height: _Optional[int] = ..., round: _Optional[int] = ..., type: _Optional[_Union[_types_pb2.SignedMsgType, str]] = ..., block_id: _Optional[_Union[_types_pb2.BlockID, _Mapping]] = ..., votes: _Optional[_Union[_types_pb2_1.BitArray, _Mapping]] = ...) -> None: ...

class VoteSetMaj23(_message.Message):
    __slots__ = ["block_id", "height", "round", "type"]
    BLOCK_ID_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    block_id: _types_pb2.BlockID
    height: int
    round: int
    type: _types_pb2.SignedMsgType
    def __init__(self, height: _Optional[int] = ..., round: _Optional[int] = ..., type: _Optional[_Union[_types_pb2.SignedMsgType, str]] = ..., block_id: _Optional[_Union[_types_pb2.BlockID, _Mapping]] = ...) -> None: ...
