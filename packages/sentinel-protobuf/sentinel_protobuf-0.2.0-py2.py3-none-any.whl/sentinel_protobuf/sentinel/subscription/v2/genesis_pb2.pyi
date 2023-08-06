from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import any_pb2 as _any_pb2
from sentinel.subscription.v2 import params_pb2 as _params_pb2
from sentinel.subscription.v2 import quota_pb2 as _quota_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ["params", "subscriptions"]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params
    subscriptions: _containers.RepeatedCompositeFieldContainer[GenesisSubscription]
    def __init__(self, subscriptions: _Optional[_Iterable[_Union[GenesisSubscription, _Mapping]]] = ..., params: _Optional[_Union[_params_pb2.Params, _Mapping]] = ...) -> None: ...

class GenesisSubscription(_message.Message):
    __slots__ = ["quotas", "subscription"]
    QUOTAS_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    quotas: _containers.RepeatedCompositeFieldContainer[_quota_pb2.Quota]
    subscription: _any_pb2.Any
    def __init__(self, subscription: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., quotas: _Optional[_Iterable[_Union[_quota_pb2.Quota, _Mapping]]] = ...) -> None: ...
