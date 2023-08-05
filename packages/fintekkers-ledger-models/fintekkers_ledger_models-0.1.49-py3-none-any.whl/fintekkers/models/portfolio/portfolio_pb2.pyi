from fintekkers.models.util import local_timestamp_pb2 as _local_timestamp_pb2
from fintekkers.models.util import uuid_pb2 as _uuid_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PortfolioProto(_message.Message):
    __slots__ = ["as_of", "is_link", "object_class", "portfolio_name", "uuid", "version"]
    AS_OF_FIELD_NUMBER: _ClassVar[int]
    IS_LINK_FIELD_NUMBER: _ClassVar[int]
    OBJECT_CLASS_FIELD_NUMBER: _ClassVar[int]
    PORTFOLIO_NAME_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    as_of: _local_timestamp_pb2.LocalTimestampProto
    is_link: bool
    object_class: str
    portfolio_name: str
    uuid: _uuid_pb2.UUIDProto
    version: str
    def __init__(self, object_class: _Optional[str] = ..., version: _Optional[str] = ..., uuid: _Optional[_Union[_uuid_pb2.UUIDProto, _Mapping]] = ..., as_of: _Optional[_Union[_local_timestamp_pb2.LocalTimestampProto, _Mapping]] = ..., is_link: bool = ..., portfolio_name: _Optional[str] = ...) -> None: ...
