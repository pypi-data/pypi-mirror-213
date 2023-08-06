from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ["inactive_duration", "proof_verification_enabled"]
    INACTIVE_DURATION_FIELD_NUMBER: _ClassVar[int]
    PROOF_VERIFICATION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    inactive_duration: _duration_pb2.Duration
    proof_verification_enabled: bool
    def __init__(self, inactive_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., proof_verification_enabled: bool = ...) -> None: ...
