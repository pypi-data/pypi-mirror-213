from gogoproto import gogo_pb2 as _gogo_pb2
from sentinel.mint.v1 import inflation_pb2 as _inflation_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ["inflations"]
    INFLATIONS_FIELD_NUMBER: _ClassVar[int]
    inflations: _containers.RepeatedCompositeFieldContainer[_inflation_pb2.Inflation]
    def __init__(self, inflations: _Optional[_Iterable[_Union[_inflation_pb2.Inflation, _Mapping]]] = ...) -> None: ...
