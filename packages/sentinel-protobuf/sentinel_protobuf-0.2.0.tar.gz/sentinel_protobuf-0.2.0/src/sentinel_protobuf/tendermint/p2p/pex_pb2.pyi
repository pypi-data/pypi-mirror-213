from tendermint.p2p import types_pb2 as _types_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Message(_message.Message):
    __slots__ = ["pex_addrs", "pex_request"]
    PEX_ADDRS_FIELD_NUMBER: _ClassVar[int]
    PEX_REQUEST_FIELD_NUMBER: _ClassVar[int]
    pex_addrs: PexAddrs
    pex_request: PexRequest
    def __init__(self, pex_request: _Optional[_Union[PexRequest, _Mapping]] = ..., pex_addrs: _Optional[_Union[PexAddrs, _Mapping]] = ...) -> None: ...

class PexAddrs(_message.Message):
    __slots__ = ["addrs"]
    ADDRS_FIELD_NUMBER: _ClassVar[int]
    addrs: _containers.RepeatedCompositeFieldContainer[_types_pb2.NetAddress]
    def __init__(self, addrs: _Optional[_Iterable[_Union[_types_pb2.NetAddress, _Mapping]]] = ...) -> None: ...

class PexRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
