from fintekkers.models.portfolio import portfolio_pb2 as _portfolio_pb2
from fintekkers.requests.portfolio import query_portfolio_request_pb2 as _query_portfolio_request_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryPortfolioResponseProto(_message.Message):
    __slots__ = ["object_class", "portfolio_response", "query_portfolio_request", "version"]
    OBJECT_CLASS_FIELD_NUMBER: _ClassVar[int]
    PORTFOLIO_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    QUERY_PORTFOLIO_REQUEST_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    object_class: str
    portfolio_response: _containers.RepeatedCompositeFieldContainer[_portfolio_pb2.PortfolioProto]
    query_portfolio_request: _query_portfolio_request_pb2.QueryPortfolioRequestProto
    version: str
    def __init__(self, object_class: _Optional[str] = ..., version: _Optional[str] = ..., query_portfolio_request: _Optional[_Union[_query_portfolio_request_pb2.QueryPortfolioRequestProto, _Mapping]] = ..., portfolio_response: _Optional[_Iterable[_Union[_portfolio_pb2.PortfolioProto, _Mapping]]] = ...) -> None: ...
