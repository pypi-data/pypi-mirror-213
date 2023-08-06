from gogoproto import gogo_pb2 as _gogo_pb2
from ibc.core.channel.v1 import channel_pb2 as _channel_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ["ack_sequences", "acknowledgements", "channels", "commitments", "next_channel_sequence", "receipts", "recv_sequences", "send_sequences"]
    ACKNOWLEDGEMENTS_FIELD_NUMBER: _ClassVar[int]
    ACK_SEQUENCES_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    COMMITMENTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CHANNEL_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    RECEIPTS_FIELD_NUMBER: _ClassVar[int]
    RECV_SEQUENCES_FIELD_NUMBER: _ClassVar[int]
    SEND_SEQUENCES_FIELD_NUMBER: _ClassVar[int]
    ack_sequences: _containers.RepeatedCompositeFieldContainer[PacketSequence]
    acknowledgements: _containers.RepeatedCompositeFieldContainer[_channel_pb2.PacketState]
    channels: _containers.RepeatedCompositeFieldContainer[_channel_pb2.IdentifiedChannel]
    commitments: _containers.RepeatedCompositeFieldContainer[_channel_pb2.PacketState]
    next_channel_sequence: int
    receipts: _containers.RepeatedCompositeFieldContainer[_channel_pb2.PacketState]
    recv_sequences: _containers.RepeatedCompositeFieldContainer[PacketSequence]
    send_sequences: _containers.RepeatedCompositeFieldContainer[PacketSequence]
    def __init__(self, channels: _Optional[_Iterable[_Union[_channel_pb2.IdentifiedChannel, _Mapping]]] = ..., acknowledgements: _Optional[_Iterable[_Union[_channel_pb2.PacketState, _Mapping]]] = ..., commitments: _Optional[_Iterable[_Union[_channel_pb2.PacketState, _Mapping]]] = ..., receipts: _Optional[_Iterable[_Union[_channel_pb2.PacketState, _Mapping]]] = ..., send_sequences: _Optional[_Iterable[_Union[PacketSequence, _Mapping]]] = ..., recv_sequences: _Optional[_Iterable[_Union[PacketSequence, _Mapping]]] = ..., ack_sequences: _Optional[_Iterable[_Union[PacketSequence, _Mapping]]] = ..., next_channel_sequence: _Optional[int] = ...) -> None: ...

class PacketSequence(_message.Message):
    __slots__ = ["channel_id", "port_id", "sequence"]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    port_id: str
    sequence: int
    def __init__(self, port_id: _Optional[str] = ..., channel_id: _Optional[str] = ..., sequence: _Optional[int] = ...) -> None: ...
