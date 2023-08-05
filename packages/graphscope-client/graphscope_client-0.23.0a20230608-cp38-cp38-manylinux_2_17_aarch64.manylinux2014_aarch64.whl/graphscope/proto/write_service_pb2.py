# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: graphscope/proto/write_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$graphscope/proto/write_service.proto\x12\x17gs.rpc.write_service.v1\"\x14\n\x12GetClientIdRequest\"(\n\x13GetClientIdResponse\x12\x11\n\tclient_id\x18\x01 \x01(\t\"g\n\x11\x42\x61tchWriteRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12?\n\x0ewrite_requests\x18\x02 \x03(\x0b\x32\'.gs.rpc.write_service.v1.WriteRequestPb\")\n\x12\x42\x61tchWriteResponse\x12\x13\n\x0bsnapshot_id\x18\x01 \x01(\x03\"?\n\x12RemoteFlushRequest\x12\x13\n\x0bsnapshot_id\x18\x01 \x01(\x03\x12\x14\n\x0cwait_time_ms\x18\x02 \x01(\x03\"&\n\x13RemoteFlushResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x86\x01\n\x0eWriteRequestPb\x12\x38\n\nwrite_type\x18\x01 \x01(\x0e\x32$.gs.rpc.write_service.v1.WriteTypePb\x12:\n\x0b\x64\x61ta_record\x18\x02 \x01(\x0b\x32%.gs.rpc.write_service.v1.DataRecordPb\"\xa8\x02\n\x0c\x44\x61taRecordPb\x12G\n\x11vertex_record_key\x18\x01 \x01(\x0b\x32*.gs.rpc.write_service.v1.VertexRecordKeyPbH\x00\x12\x43\n\x0f\x65\x64ge_record_key\x18\x02 \x01(\x0b\x32(.gs.rpc.write_service.v1.EdgeRecordKeyPbH\x00\x12I\n\nproperties\x18\x03 \x03(\x0b\x32\x35.gs.rpc.write_service.v1.DataRecordPb.PropertiesEntry\x1a\x31\n\x0fPropertiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x0c\n\nrecord_key\"\xac\x01\n\x11VertexRecordKeyPb\x12\r\n\x05label\x18\x01 \x01(\t\x12S\n\rpk_properties\x18\x02 \x03(\x0b\x32<.gs.rpc.write_service.v1.VertexRecordKeyPb.PkPropertiesEntry\x1a\x33\n\x11PkPropertiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xba\x01\n\x0f\x45\x64geRecordKeyPb\x12\r\n\x05label\x18\x01 \x01(\t\x12\x42\n\x0esrc_vertex_key\x18\x02 \x01(\x0b\x32*.gs.rpc.write_service.v1.VertexRecordKeyPb\x12\x42\n\x0e\x64st_vertex_key\x18\x03 \x01(\x0b\x32*.gs.rpc.write_service.v1.VertexRecordKeyPb\x12\x10\n\x08inner_id\x18\x04 \x01(\x03*>\n\x0bWriteTypePb\x12\x0b\n\x07UNKNOWN\x10\x00\x12\n\n\x06INSERT\x10\x01\x12\n\n\x06UPDATE\x10\x02\x12\n\n\x06\x44\x45LETE\x10\x03\x32\xc8\x02\n\x0b\x43lientWrite\x12h\n\x0bgetClientId\x12+.gs.rpc.write_service.v1.GetClientIdRequest\x1a,.gs.rpc.write_service.v1.GetClientIdResponse\x12\x65\n\nbatchWrite\x12*.gs.rpc.write_service.v1.BatchWriteRequest\x1a+.gs.rpc.write_service.v1.BatchWriteResponse\x12h\n\x0bremoteFlush\x12+.gs.rpc.write_service.v1.RemoteFlushRequest\x1a,.gs.rpc.write_service.v1.RemoteFlushResponseB&\n\"com.alibaba.graphscope.proto.writeP\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'graphscope.proto.write_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\"com.alibaba.graphscope.proto.writeP\001'
  _DATARECORDPB_PROPERTIESENTRY._options = None
  _DATARECORDPB_PROPERTIESENTRY._serialized_options = b'8\001'
  _VERTEXRECORDKEYPB_PKPROPERTIESENTRY._options = None
  _VERTEXRECORDKEYPB_PKPROPERTIESENTRY._serialized_options = b'8\001'
  _WRITETYPEPB._serialized_start=1182
  _WRITETYPEPB._serialized_end=1244
  _GETCLIENTIDREQUEST._serialized_start=65
  _GETCLIENTIDREQUEST._serialized_end=85
  _GETCLIENTIDRESPONSE._serialized_start=87
  _GETCLIENTIDRESPONSE._serialized_end=127
  _BATCHWRITEREQUEST._serialized_start=129
  _BATCHWRITEREQUEST._serialized_end=232
  _BATCHWRITERESPONSE._serialized_start=234
  _BATCHWRITERESPONSE._serialized_end=275
  _REMOTEFLUSHREQUEST._serialized_start=277
  _REMOTEFLUSHREQUEST._serialized_end=340
  _REMOTEFLUSHRESPONSE._serialized_start=342
  _REMOTEFLUSHRESPONSE._serialized_end=380
  _WRITEREQUESTPB._serialized_start=383
  _WRITEREQUESTPB._serialized_end=517
  _DATARECORDPB._serialized_start=520
  _DATARECORDPB._serialized_end=816
  _DATARECORDPB_PROPERTIESENTRY._serialized_start=753
  _DATARECORDPB_PROPERTIESENTRY._serialized_end=802
  _VERTEXRECORDKEYPB._serialized_start=819
  _VERTEXRECORDKEYPB._serialized_end=991
  _VERTEXRECORDKEYPB_PKPROPERTIESENTRY._serialized_start=940
  _VERTEXRECORDKEYPB_PKPROPERTIESENTRY._serialized_end=991
  _EDGERECORDKEYPB._serialized_start=994
  _EDGERECORDKEYPB._serialized_end=1180
  _CLIENTWRITE._serialized_start=1247
  _CLIENTWRITE._serialized_end=1575
# @@protoc_insertion_point(module_scope)
