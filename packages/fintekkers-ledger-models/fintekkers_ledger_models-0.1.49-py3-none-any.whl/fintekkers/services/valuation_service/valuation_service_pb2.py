# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fintekkers/services/valuation-service/valuation_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from fintekkers.requests.valuation import valuation_request_pb2 as fintekkers_dot_requests_dot_valuation_dot_valuation__request__pb2
from fintekkers.requests.valuation import valuation_response_pb2 as fintekkers_dot_requests_dot_valuation_dot_valuation__response__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n=fintekkers/services/valuation-service/valuation_service.proto\x12%fintekkers.services.valuation_service\x1a\x35\x66intekkers/requests/valuation/valuation_request.proto\x1a\x36\x66intekkers/requests/valuation/valuation_response.proto2\x88\x01\n\tValuation\x12{\n\x0cRunValuation\x12\x34.fintekkers.requests.valuation.ValuationRequestProto\x1a\x35.fintekkers.requests.valuation.ValuationResponseProtoB\x06\x88\x01\x01\x90\x01\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fintekkers.services.valuation_service.valuation_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\210\001\001\220\001\001'
  _VALUATION._serialized_start=216
  _VALUATION._serialized_end=352
_builder.BuildServices(DESCRIPTOR, 'fintekkers.services.valuation_service.valuation_service_pb2', globals())
# @@protoc_insertion_point(module_scope)
