from gogoproto import gogo_pb2 as _gogo_pb2
from sentinel.node.v2 import node_pb2 as _node_pb2
from sentinel.node.v2 import params_pb2 as _params_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ["nodes", "params"]
    NODES_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[_node_pb2.Node]
    params: _params_pb2.Params
    def __init__(self, nodes: _Optional[_Iterable[_Union[_node_pb2.Node, _Mapping]]] = ..., params: _Optional[_Union[_params_pb2.Params, _Mapping]] = ...) -> None: ...
