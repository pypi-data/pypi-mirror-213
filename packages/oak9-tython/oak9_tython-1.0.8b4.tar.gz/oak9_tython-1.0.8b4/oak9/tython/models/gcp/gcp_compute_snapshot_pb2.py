# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gcp/gcp_compute_snapshot.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1egcp/gcp_compute_snapshot.proto\x12 oak9.tython.gcp.compute_snapshot\x1a\x13shared/shared.proto\"\x84\x01\n%ComputeSnapshotXSnapshotEncryptionKey\x12\x19\n\x11kms_key_self_link\x18\x01 \x01(\t\x12\x1f\n\x17kms_key_service_account\x18\x02 \x01(\t\x12\x0f\n\x07raw_key\x18\x03 \x01(\t\x12\x0e\n\x06sha256\x18\x04 \x01(\t\"[\n\'ComputeSnapshotXSourceDiskEncryptionKey\x12\x1f\n\x17kms_key_service_account\x18\x01 \x01(\t\x12\x0f\n\x07raw_key\x18\x02 \x01(\t\"J\n\x18\x43omputeSnapshotXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\x12\x0e\n\x06update\x18\x03 \x01(\t\"\x8b\x06\n\x0f\x43omputeSnapshot\x12\x1a\n\x12\x63reation_timestamp\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x14\n\x0c\x64isk_size_gb\x18\x03 \x01(\x01\x12\n\n\x02id\x18\x04 \x01(\t\x12\x19\n\x11label_fingerprint\x18\x05 \x01(\t\x12M\n\x06labels\x18\x06 \x03(\x0b\x32=.oak9.tython.gcp.compute_snapshot.ComputeSnapshot.LabelsEntry\x12\x10\n\x08licenses\x18\x07 \x03(\t\x12\x0c\n\x04name\x18\x08 \x01(\t\x12\x0f\n\x07project\x18\t \x01(\t\x12\x11\n\tself_link\x18\n \x01(\t\x12\x13\n\x0bsnapshot_id\x18\x0b \x01(\x01\x12\x13\n\x0bsource_disk\x18\x0c \x01(\t\x12\x15\n\rstorage_bytes\x18\r \x01(\x01\x12\x19\n\x11storage_locations\x18\x0e \x03(\t\x12\x0c\n\x04zone\x18\x0f \x01(\t\x12h\n\x17snapshot_encryption_key\x18\x10 \x01(\x0b\x32G.oak9.tython.gcp.compute_snapshot.ComputeSnapshotXSnapshotEncryptionKey\x12m\n\x1asource_disk_encryption_key\x18\x11 \x01(\x0b\x32I.oak9.tython.gcp.compute_snapshot.ComputeSnapshotXSourceDiskEncryptionKey\x12L\n\x08timeouts\x18\x12 \x01(\x0b\x32:.oak9.tython.gcp.compute_snapshot.ComputeSnapshotXTimeouts\x12\x37\n\rresource_info\x18\x13 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"]\n#ComputeSnapshotIamBindingXCondition\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12\x12\n\nexpression\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\"\x86\x02\n\x19\x43omputeSnapshotIamBinding\x12\x0c\n\x04\x65tag\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07members\x18\x03 \x03(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x0f\n\x07project\x18\x05 \x01(\t\x12\x0c\n\x04role\x18\x06 \x01(\t\x12X\n\tcondition\x18\x07 \x01(\x0b\x32\x45.oak9.tython.gcp.compute_snapshot.ComputeSnapshotIamBindingXCondition\x12\x37\n\rresource_info\x18\x08 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\\\n\"ComputeSnapshotIamMemberXCondition\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12\x12\n\nexpression\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\"\x83\x02\n\x18\x43omputeSnapshotIamMember\x12\x0c\n\x04\x65tag\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0e\n\x06member\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x0f\n\x07project\x18\x05 \x01(\t\x12\x0c\n\x04role\x18\x06 \x01(\t\x12W\n\tcondition\x18\x07 \x01(\x0b\x32\x44.oak9.tython.gcp.compute_snapshot.ComputeSnapshotIamMemberXCondition\x12\x37\n\rresource_info\x18\x08 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xa1\x01\n\x18\x43omputeSnapshotIamPolicy\x12\x0c\n\x04\x65tag\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x13\n\x0bpolicy_data\x18\x04 \x01(\t\x12\x0f\n\x07project\x18\x05 \x01(\t\x12\x37\n\rresource_info\x18\x06 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gcp.gcp_compute_snapshot_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _COMPUTESNAPSHOT_LABELSENTRY._options = None
  _COMPUTESNAPSHOT_LABELSENTRY._serialized_options = b'8\001'
  _COMPUTESNAPSHOTXSNAPSHOTENCRYPTIONKEY._serialized_start=90
  _COMPUTESNAPSHOTXSNAPSHOTENCRYPTIONKEY._serialized_end=222
  _COMPUTESNAPSHOTXSOURCEDISKENCRYPTIONKEY._serialized_start=224
  _COMPUTESNAPSHOTXSOURCEDISKENCRYPTIONKEY._serialized_end=315
  _COMPUTESNAPSHOTXTIMEOUTS._serialized_start=317
  _COMPUTESNAPSHOTXTIMEOUTS._serialized_end=391
  _COMPUTESNAPSHOT._serialized_start=394
  _COMPUTESNAPSHOT._serialized_end=1173
  _COMPUTESNAPSHOT_LABELSENTRY._serialized_start=1128
  _COMPUTESNAPSHOT_LABELSENTRY._serialized_end=1173
  _COMPUTESNAPSHOTIAMBINDINGXCONDITION._serialized_start=1175
  _COMPUTESNAPSHOTIAMBINDINGXCONDITION._serialized_end=1268
  _COMPUTESNAPSHOTIAMBINDING._serialized_start=1271
  _COMPUTESNAPSHOTIAMBINDING._serialized_end=1533
  _COMPUTESNAPSHOTIAMMEMBERXCONDITION._serialized_start=1535
  _COMPUTESNAPSHOTIAMMEMBERXCONDITION._serialized_end=1627
  _COMPUTESNAPSHOTIAMMEMBER._serialized_start=1630
  _COMPUTESNAPSHOTIAMMEMBER._serialized_end=1889
  _COMPUTESNAPSHOTIAMPOLICY._serialized_start=1892
  _COMPUTESNAPSHOTIAMPOLICY._serialized_end=2053
# @@protoc_insertion_point(module_scope)
