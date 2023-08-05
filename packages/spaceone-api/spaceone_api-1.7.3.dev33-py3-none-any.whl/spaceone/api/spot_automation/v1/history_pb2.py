# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/spot_automation/v1/history.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from spaceone.api.core.v1 import query_pb2 as spaceone_dot_api_dot_core_dot_v1_dot_query__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='spaceone/api/spot_automation/v1/history.proto',
  package='spaceone.api.spot_automation.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n-spaceone/api/spot_automation/v1/history.proto\x12\x1fspaceone.api.spot_automation.v1\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"k\n\x13QueryHistoryRequest\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x15\n\rspot_group_id\x18\x02 \x01(\t\x12\x11\n\tdomain_id\x18\n \x01(\t\"]\n\x12HistoryStatRequest\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"\xcd\x01\n\x10HistoryValueInfo\x12\x12\n\nhistory_id\x18\x01 \x01(\t\x12\x15\n\rspot_group_id\x18\x02 \x01(\t\x12\x16\n\x0eondemand_count\x18\x03 \x01(\x05\x12\x12\n\nspot_count\x18\x04 \x01(\x05\x12\x13\n\x0btotal_count\x18\x05 \x01(\x05\x12\x12\n\nproject_id\x18\x06 \x01(\t\x12\x11\n\tdomain_id\x18\x07 \x01(\t\x12\x12\n\nhistory_at\x18\x08 \x01(\t\x12\x12\n\ncreated_at\x18\t \x01(\t\"f\n\x0bHistoryInfo\x12\x42\n\x07results\x18\x01 \x03(\x0b\x32\x31.spaceone.api.spot_automation.v1.HistoryValueInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\x32\xc1\x02\n\x07History\x12\xb5\x01\n\x04list\x12\x34.spaceone.api.spot_automation.v1.QueryHistoryRequest\x1a,.spaceone.api.spot_automation.v1.HistoryInfo\"I\x82\xd3\xe4\x93\x02\x43\x12\x1b/spot-automation/v1/historyZ$\"\"/spot-automation/v1/history/search\x12~\n\x04stat\x12\x33.spaceone.api.spot_automation.v1.HistoryStatRequest\x1a\x17.google.protobuf.Struct\"(\x82\xd3\xe4\x93\x02\"\" /spot-automation/v1/history/statb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,spaceone_dot_api_dot_core_dot_v1_dot_query__pb2.DESCRIPTOR,])




_QUERYHISTORYREQUEST = _descriptor.Descriptor(
  name='QueryHistoryRequest',
  full_name='spaceone.api.spot_automation.v1.QueryHistoryRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='query', full_name='spaceone.api.spot_automation.v1.QueryHistoryRequest.query', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='spot_group_id', full_name='spaceone.api.spot_automation.v1.QueryHistoryRequest.spot_group_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.spot_automation.v1.QueryHistoryRequest.domain_id', index=2,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  ],
  serialized_start=176,
  serialized_end=283,
)


_HISTORYSTATREQUEST = _descriptor.Descriptor(
  name='HistoryStatRequest',
  full_name='spaceone.api.spot_automation.v1.HistoryStatRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='query', full_name='spaceone.api.spot_automation.v1.HistoryStatRequest.query', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.spot_automation.v1.HistoryStatRequest.domain_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  ],
  serialized_start=285,
  serialized_end=378,
)


_HISTORYVALUEINFO = _descriptor.Descriptor(
  name='HistoryValueInfo',
  full_name='spaceone.api.spot_automation.v1.HistoryValueInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='history_id', full_name='spaceone.api.spot_automation.v1.HistoryValueInfo.history_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='spot_group_id', full_name='spaceone.api.spot_automation.v1.HistoryValueInfo.spot_group_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ondemand_count', full_name='spaceone.api.spot_automation.v1.HistoryValueInfo.ondemand_count', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='spot_count', full_name='spaceone.api.spot_automation.v1.HistoryValueInfo.spot_count', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='total_count', full_name='spaceone.api.spot_automation.v1.HistoryValueInfo.total_count', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='project_id', full_name='spaceone.api.spot_automation.v1.HistoryValueInfo.project_id', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.spot_automation.v1.HistoryValueInfo.domain_id', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='history_at', full_name='spaceone.api.spot_automation.v1.HistoryValueInfo.history_at', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='spaceone.api.spot_automation.v1.HistoryValueInfo.created_at', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  ],
  serialized_start=381,
  serialized_end=586,
)


_HISTORYINFO = _descriptor.Descriptor(
  name='HistoryInfo',
  full_name='spaceone.api.spot_automation.v1.HistoryInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='results', full_name='spaceone.api.spot_automation.v1.HistoryInfo.results', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='total_count', full_name='spaceone.api.spot_automation.v1.HistoryInfo.total_count', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  ],
  serialized_start=588,
  serialized_end=690,
)

_QUERYHISTORYREQUEST.fields_by_name['query'].message_type = spaceone_dot_api_dot_core_dot_v1_dot_query__pb2._QUERY
_HISTORYSTATREQUEST.fields_by_name['query'].message_type = spaceone_dot_api_dot_core_dot_v1_dot_query__pb2._STATISTICSQUERY
_HISTORYINFO.fields_by_name['results'].message_type = _HISTORYVALUEINFO
DESCRIPTOR.message_types_by_name['QueryHistoryRequest'] = _QUERYHISTORYREQUEST
DESCRIPTOR.message_types_by_name['HistoryStatRequest'] = _HISTORYSTATREQUEST
DESCRIPTOR.message_types_by_name['HistoryValueInfo'] = _HISTORYVALUEINFO
DESCRIPTOR.message_types_by_name['HistoryInfo'] = _HISTORYINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

QueryHistoryRequest = _reflection.GeneratedProtocolMessageType('QueryHistoryRequest', (_message.Message,), {
  'DESCRIPTOR' : _QUERYHISTORYREQUEST,
  '__module__' : 'spaceone.api.spot_automation.v1.history_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.spot_automation.v1.QueryHistoryRequest)
  })
_sym_db.RegisterMessage(QueryHistoryRequest)

HistoryStatRequest = _reflection.GeneratedProtocolMessageType('HistoryStatRequest', (_message.Message,), {
  'DESCRIPTOR' : _HISTORYSTATREQUEST,
  '__module__' : 'spaceone.api.spot_automation.v1.history_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.spot_automation.v1.HistoryStatRequest)
  })
_sym_db.RegisterMessage(HistoryStatRequest)

HistoryValueInfo = _reflection.GeneratedProtocolMessageType('HistoryValueInfo', (_message.Message,), {
  'DESCRIPTOR' : _HISTORYVALUEINFO,
  '__module__' : 'spaceone.api.spot_automation.v1.history_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.spot_automation.v1.HistoryValueInfo)
  })
_sym_db.RegisterMessage(HistoryValueInfo)

HistoryInfo = _reflection.GeneratedProtocolMessageType('HistoryInfo', (_message.Message,), {
  'DESCRIPTOR' : _HISTORYINFO,
  '__module__' : 'spaceone.api.spot_automation.v1.history_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.spot_automation.v1.HistoryInfo)
  })
_sym_db.RegisterMessage(HistoryInfo)



_HISTORY = _descriptor.ServiceDescriptor(
  name='History',
  full_name='spaceone.api.spot_automation.v1.History',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=693,
  serialized_end=1014,
  methods=[
  _descriptor.MethodDescriptor(
    name='list',
    full_name='spaceone.api.spot_automation.v1.History.list',
    index=0,
    containing_service=None,
    input_type=_QUERYHISTORYREQUEST,
    output_type=_HISTORYINFO,
    serialized_options=b'\202\323\344\223\002C\022\033/spot-automation/v1/historyZ$\"\"/spot-automation/v1/history/search',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='stat',
    full_name='spaceone.api.spot_automation.v1.History.stat',
    index=1,
    containing_service=None,
    input_type=_HISTORYSTATREQUEST,
    output_type=google_dot_protobuf_dot_struct__pb2._STRUCT,
    serialized_options=b'\202\323\344\223\002\"\" /spot-automation/v1/history/stat',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_HISTORY)

DESCRIPTOR.services_by_name['History'] = _HISTORY

# @@protoc_insertion_point(module_scope)
