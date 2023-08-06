from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor
STATUS_ACTIVE: Status
STATUS_INACTIVE: Status
STATUS_INACTIVE_PENDING: Status
STATUS_UNSPECIFIED: Status

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
