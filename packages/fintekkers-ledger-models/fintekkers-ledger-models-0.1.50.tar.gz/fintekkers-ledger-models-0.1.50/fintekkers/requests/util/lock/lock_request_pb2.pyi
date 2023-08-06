from fintekkers.models.util.lock import node_partition_pb2 as _node_partition_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LockRequestProto(_message.Message):
    __slots__ = ["node_partition", "object_class", "version"]
    NODE_PARTITION_FIELD_NUMBER: _ClassVar[int]
    OBJECT_CLASS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    node_partition: _node_partition_pb2.NodePartition
    object_class: str
    version: str
    def __init__(self, object_class: _Optional[str] = ..., version: _Optional[str] = ..., node_partition: _Optional[_Union[_node_partition_pb2.NodePartition, _Mapping]] = ...) -> None: ...
