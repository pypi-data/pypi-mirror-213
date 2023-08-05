from fintekkers.models.price import price_pb2 as _price_pb2
from fintekkers.requests.price import create_price_request_pb2 as _create_price_request_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreatePriceResponseProto(_message.Message):
    __slots__ = ["create_price_request", "object_class", "price_response", "version"]
    CREATE_PRICE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    OBJECT_CLASS_FIELD_NUMBER: _ClassVar[int]
    PRICE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    create_price_request: _create_price_request_pb2.CreatePriceRequestProto
    object_class: str
    price_response: _containers.RepeatedCompositeFieldContainer[_price_pb2.PriceProto]
    version: str
    def __init__(self, object_class: _Optional[str] = ..., version: _Optional[str] = ..., create_price_request: _Optional[_Union[_create_price_request_pb2.CreatePriceRequestProto, _Mapping]] = ..., price_response: _Optional[_Iterable[_Union[_price_pb2.PriceProto, _Mapping]]] = ...) -> None: ...
