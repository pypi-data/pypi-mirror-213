from fintekkers.models.price import price_pb2 as _price_pb2
from fintekkers.requests.price import query_price_request_pb2 as _query_price_request_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryPriceResponseProto(_message.Message):
    __slots__ = ["object_class", "price_response", "query_price_request", "version"]
    OBJECT_CLASS_FIELD_NUMBER: _ClassVar[int]
    PRICE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    QUERY_PRICE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    object_class: str
    price_response: _containers.RepeatedCompositeFieldContainer[_price_pb2.PriceProto]
    query_price_request: _query_price_request_pb2.QueryPriceRequestProto
    version: str
    def __init__(self, object_class: _Optional[str] = ..., version: _Optional[str] = ..., query_price_request: _Optional[_Union[_query_price_request_pb2.QueryPriceRequestProto, _Mapping]] = ..., price_response: _Optional[_Iterable[_Union[_price_pb2.PriceProto, _Mapping]]] = ...) -> None: ...
