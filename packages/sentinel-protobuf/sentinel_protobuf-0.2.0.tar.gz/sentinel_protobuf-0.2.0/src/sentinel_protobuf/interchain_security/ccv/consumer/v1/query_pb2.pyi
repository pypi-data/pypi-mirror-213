from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NextFeeDistributionEstimate(_message.Message):
    __slots__ = ["currentHeight", "distribution_fraction", "lastHeight", "nextHeight", "toConsumer", "toProvider", "total"]
    CURRENTHEIGHT_FIELD_NUMBER: _ClassVar[int]
    DISTRIBUTION_FRACTION_FIELD_NUMBER: _ClassVar[int]
    LASTHEIGHT_FIELD_NUMBER: _ClassVar[int]
    NEXTHEIGHT_FIELD_NUMBER: _ClassVar[int]
    TOCONSUMER_FIELD_NUMBER: _ClassVar[int]
    TOPROVIDER_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    currentHeight: int
    distribution_fraction: str
    lastHeight: int
    nextHeight: int
    toConsumer: str
    toProvider: str
    total: str
    def __init__(self, currentHeight: _Optional[int] = ..., lastHeight: _Optional[int] = ..., nextHeight: _Optional[int] = ..., distribution_fraction: _Optional[str] = ..., total: _Optional[str] = ..., toProvider: _Optional[str] = ..., toConsumer: _Optional[str] = ...) -> None: ...

class QueryNextFeeDistributionEstimateRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class QueryNextFeeDistributionEstimateResponse(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: NextFeeDistributionEstimate
    def __init__(self, data: _Optional[_Union[NextFeeDistributionEstimate, _Mapping]] = ...) -> None: ...
