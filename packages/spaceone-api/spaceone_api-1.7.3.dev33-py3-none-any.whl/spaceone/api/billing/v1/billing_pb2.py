# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/billing/v1/billing.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='spaceone/api/billing/v1/billing.proto',
  package='spaceone.api.billing.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n%spaceone/api/billing/v1/billing.proto\x12\x17spaceone.api.billing.v1\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\"\xa3\x02\n\x12\x42illingDataRequest\x12\x14\n\nproject_id\x18\x01 \x01(\tH\x00\x12\x1a\n\x10project_group_id\x18\x02 \x01(\tH\x00\x12\x18\n\x10service_accounts\x18\x03 \x03(\t\x12\'\n\x06\x66ilter\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x13\n\x0b\x61ggregation\x18\x05 \x03(\t\x12\r\n\x05start\x18\x06 \x01(\t\x12\x0b\n\x03\x65nd\x18\x07 \x01(\t\x12\x13\n\x0bgranularity\x18\x08 \x01(\t\x12\x11\n\tdomain_id\x18\t \x01(\t\x12%\n\x04sort\x18\n \x01(\x0b\x32\x17.google.protobuf.Struct\x12\r\n\x05limit\x18\x0b \x01(\x05\x42\t\n\x07project2\x81\x01\n\x07\x42illing\x12v\n\x08get_data\x12+.spaceone.api.billing.v1.BillingDataRequest\x1a\x17.google.protobuf.Struct\"$\x82\xd3\xe4\x93\x02\x1e\x12\x1c/billing/v1/billing/get-datab\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_BILLINGDATAREQUEST = _descriptor.Descriptor(
  name='BillingDataRequest',
  full_name='spaceone.api.billing.v1.BillingDataRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='project_id', full_name='spaceone.api.billing.v1.BillingDataRequest.project_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='project_group_id', full_name='spaceone.api.billing.v1.BillingDataRequest.project_group_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='service_accounts', full_name='spaceone.api.billing.v1.BillingDataRequest.service_accounts', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filter', full_name='spaceone.api.billing.v1.BillingDataRequest.filter', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='aggregation', full_name='spaceone.api.billing.v1.BillingDataRequest.aggregation', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start', full_name='spaceone.api.billing.v1.BillingDataRequest.start', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end', full_name='spaceone.api.billing.v1.BillingDataRequest.end', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='granularity', full_name='spaceone.api.billing.v1.BillingDataRequest.granularity', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.billing.v1.BillingDataRequest.domain_id', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sort', full_name='spaceone.api.billing.v1.BillingDataRequest.sort', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='limit', full_name='spaceone.api.billing.v1.BillingDataRequest.limit', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='project', full_name='spaceone.api.billing.v1.BillingDataRequest.project',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=127,
  serialized_end=418,
)

_BILLINGDATAREQUEST.fields_by_name['filter'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_BILLINGDATAREQUEST.fields_by_name['sort'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_BILLINGDATAREQUEST.oneofs_by_name['project'].fields.append(
  _BILLINGDATAREQUEST.fields_by_name['project_id'])
_BILLINGDATAREQUEST.fields_by_name['project_id'].containing_oneof = _BILLINGDATAREQUEST.oneofs_by_name['project']
_BILLINGDATAREQUEST.oneofs_by_name['project'].fields.append(
  _BILLINGDATAREQUEST.fields_by_name['project_group_id'])
_BILLINGDATAREQUEST.fields_by_name['project_group_id'].containing_oneof = _BILLINGDATAREQUEST.oneofs_by_name['project']
DESCRIPTOR.message_types_by_name['BillingDataRequest'] = _BILLINGDATAREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BillingDataRequest = _reflection.GeneratedProtocolMessageType('BillingDataRequest', (_message.Message,), {
  'DESCRIPTOR' : _BILLINGDATAREQUEST,
  '__module__' : 'spaceone.api.billing.v1.billing_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.billing.v1.BillingDataRequest)
  })
_sym_db.RegisterMessage(BillingDataRequest)



_BILLING = _descriptor.ServiceDescriptor(
  name='Billing',
  full_name='spaceone.api.billing.v1.Billing',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=421,
  serialized_end=550,
  methods=[
  _descriptor.MethodDescriptor(
    name='get_data',
    full_name='spaceone.api.billing.v1.Billing.get_data',
    index=0,
    containing_service=None,
    input_type=_BILLINGDATAREQUEST,
    output_type=google_dot_protobuf_dot_struct__pb2._STRUCT,
    serialized_options=b'\202\323\344\223\002\036\022\034/billing/v1/billing/get-data',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_BILLING)

DESCRIPTOR.services_by_name['Billing'] = _BILLING

# @@protoc_insertion_point(module_scope)
