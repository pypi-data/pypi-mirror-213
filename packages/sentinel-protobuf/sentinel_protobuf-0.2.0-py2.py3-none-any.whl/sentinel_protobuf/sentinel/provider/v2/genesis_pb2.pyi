from gogoproto import gogo_pb2 as _gogo_pb2
from sentinel.provider.v2 import params_pb2 as _params_pb2
from sentinel.provider.v2 import provider_pb2 as _provider_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ["params", "providers"]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params
    providers: _containers.RepeatedCompositeFieldContainer[_provider_pb2.Provider]
    def __init__(self, providers: _Optional[_Iterable[_Union[_provider_pb2.Provider, _Mapping]]] = ..., params: _Optional[_Union[_params_pb2.Params, _Mapping]] = ...) -> None: ...
