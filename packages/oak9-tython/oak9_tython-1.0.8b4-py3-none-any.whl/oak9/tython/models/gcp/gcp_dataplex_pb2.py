# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gcp/gcp_dataplex.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16gcp/gcp_dataplex.proto\x12\x18oak9.tython.gcp.dataplex\x1a\x13shared/shared.proto\")\n\x16\x44\x61taplexLakeXMetastore\x12\x0f\n\x07service\x18\x01 \x01(\t\"G\n\x15\x44\x61taplexLakeXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\x12\x0e\n\x06update\x18\x03 \x01(\t\"\x9b\x06\n\x0c\x44\x61taplexLake\x12M\n\x0c\x61sset_status\x18\x01 \x03(\x0b\x32\x37.oak9.tython.gcp.dataplex.DataplexLake.AssetStatusEntry\x12\x13\n\x0b\x63reate_time\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x04 \x01(\t\x12\n\n\x02id\x18\x05 \x01(\t\x12\x42\n\x06labels\x18\x06 \x03(\x0b\x32\x32.oak9.tython.gcp.dataplex.DataplexLake.LabelsEntry\x12\x10\n\x08location\x18\x07 \x01(\t\x12U\n\x10metastore_status\x18\x08 \x03(\x0b\x32;.oak9.tython.gcp.dataplex.DataplexLake.MetastoreStatusEntry\x12\x0c\n\x04name\x18\t \x01(\t\x12\x0f\n\x07project\x18\n \x01(\t\x12\x17\n\x0fservice_account\x18\x0b \x01(\t\x12\r\n\x05state\x18\x0c \x01(\t\x12\x0b\n\x03uid\x18\r \x01(\t\x12\x13\n\x0bupdate_time\x18\x0e \x01(\t\x12\x43\n\tmetastore\x18\x0f \x01(\x0b\x32\x30.oak9.tython.gcp.dataplex.DataplexLakeXMetastore\x12\x41\n\x08timeouts\x18\x10 \x01(\x0b\x32/.oak9.tython.gcp.dataplex.DataplexLakeXTimeouts\x12\x37\n\rresource_info\x18\x11 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x1a\x32\n\x10\x41ssetStatusEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x36\n\x14MetastoreStatusEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x81\x01\n%DataplexZoneXDiscoverySpecXCsvOptions\x12\x11\n\tdelimiter\x18\x01 \x01(\t\x12\x1e\n\x16\x64isable_type_inference\x18\x02 \x01(\x08\x12\x10\n\x08\x65ncoding\x18\x03 \x01(\t\x12\x13\n\x0bheader_rows\x18\x04 \x01(\x01\"Z\n&DataplexZoneXDiscoverySpecXJsonOptions\x12\x1e\n\x16\x64isable_type_inference\x18\x01 \x01(\x08\x12\x10\n\x08\x65ncoding\x18\x02 \x01(\t\"\xa1\x02\n\x1a\x44\x61taplexZoneXDiscoverySpec\x12\x0f\n\x07\x65nabled\x18\x01 \x01(\x08\x12\x18\n\x10\x65xclude_patterns\x18\x02 \x03(\t\x12\x18\n\x10include_patterns\x18\x03 \x03(\t\x12\x10\n\x08schedule\x18\x04 \x01(\t\x12T\n\x0b\x63sv_options\x18\x05 \x01(\x0b\x32?.oak9.tython.gcp.dataplex.DataplexZoneXDiscoverySpecXCsvOptions\x12V\n\x0cjson_options\x18\x06 \x01(\x0b\x32@.oak9.tython.gcp.dataplex.DataplexZoneXDiscoverySpecXJsonOptions\"2\n\x19\x44\x61taplexZoneXResourceSpec\x12\x15\n\rlocation_type\x18\x01 \x01(\t\"G\n\x15\x44\x61taplexZoneXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\x12\x0e\n\x06update\x18\x03 \x01(\t\"\xe4\x05\n\x0c\x44\x61taplexZone\x12M\n\x0c\x61sset_status\x18\x01 \x03(\x0b\x32\x37.oak9.tython.gcp.dataplex.DataplexZone.AssetStatusEntry\x12\x13\n\x0b\x63reate_time\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x04 \x01(\t\x12\n\n\x02id\x18\x05 \x01(\t\x12\x42\n\x06labels\x18\x06 \x03(\x0b\x32\x32.oak9.tython.gcp.dataplex.DataplexZone.LabelsEntry\x12\x0c\n\x04lake\x18\x07 \x01(\t\x12\x10\n\x08location\x18\x08 \x01(\t\x12\x0c\n\x04name\x18\t \x01(\t\x12\x0f\n\x07project\x18\n \x01(\t\x12\r\n\x05state\x18\x0b \x01(\t\x12\x0c\n\x04type\x18\x0c \x01(\t\x12\x0b\n\x03uid\x18\r \x01(\t\x12\x13\n\x0bupdate_time\x18\x0e \x01(\t\x12L\n\x0e\x64iscovery_spec\x18\x0f \x01(\x0b\x32\x34.oak9.tython.gcp.dataplex.DataplexZoneXDiscoverySpec\x12J\n\rresource_spec\x18\x10 \x01(\x0b\x32\x33.oak9.tython.gcp.dataplex.DataplexZoneXResourceSpec\x12\x41\n\x08timeouts\x18\x11 \x01(\x0b\x32/.oak9.tython.gcp.dataplex.DataplexZoneXTimeouts\x12\x37\n\rresource_info\x18\x12 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x1a\x32\n\x10\x41ssetStatusEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gcp.gcp_dataplex_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _DATAPLEXLAKE_ASSETSTATUSENTRY._options = None
  _DATAPLEXLAKE_ASSETSTATUSENTRY._serialized_options = b'8\001'
  _DATAPLEXLAKE_LABELSENTRY._options = None
  _DATAPLEXLAKE_LABELSENTRY._serialized_options = b'8\001'
  _DATAPLEXLAKE_METASTORESTATUSENTRY._options = None
  _DATAPLEXLAKE_METASTORESTATUSENTRY._serialized_options = b'8\001'
  _DATAPLEXZONE_ASSETSTATUSENTRY._options = None
  _DATAPLEXZONE_ASSETSTATUSENTRY._serialized_options = b'8\001'
  _DATAPLEXZONE_LABELSENTRY._options = None
  _DATAPLEXZONE_LABELSENTRY._serialized_options = b'8\001'
  _DATAPLEXLAKEXMETASTORE._serialized_start=73
  _DATAPLEXLAKEXMETASTORE._serialized_end=114
  _DATAPLEXLAKEXTIMEOUTS._serialized_start=116
  _DATAPLEXLAKEXTIMEOUTS._serialized_end=187
  _DATAPLEXLAKE._serialized_start=190
  _DATAPLEXLAKE._serialized_end=985
  _DATAPLEXLAKE_ASSETSTATUSENTRY._serialized_start=832
  _DATAPLEXLAKE_ASSETSTATUSENTRY._serialized_end=882
  _DATAPLEXLAKE_LABELSENTRY._serialized_start=884
  _DATAPLEXLAKE_LABELSENTRY._serialized_end=929
  _DATAPLEXLAKE_METASTORESTATUSENTRY._serialized_start=931
  _DATAPLEXLAKE_METASTORESTATUSENTRY._serialized_end=985
  _DATAPLEXZONEXDISCOVERYSPECXCSVOPTIONS._serialized_start=988
  _DATAPLEXZONEXDISCOVERYSPECXCSVOPTIONS._serialized_end=1117
  _DATAPLEXZONEXDISCOVERYSPECXJSONOPTIONS._serialized_start=1119
  _DATAPLEXZONEXDISCOVERYSPECXJSONOPTIONS._serialized_end=1209
  _DATAPLEXZONEXDISCOVERYSPEC._serialized_start=1212
  _DATAPLEXZONEXDISCOVERYSPEC._serialized_end=1501
  _DATAPLEXZONEXRESOURCESPEC._serialized_start=1503
  _DATAPLEXZONEXRESOURCESPEC._serialized_end=1553
  _DATAPLEXZONEXTIMEOUTS._serialized_start=1555
  _DATAPLEXZONEXTIMEOUTS._serialized_end=1626
  _DATAPLEXZONE._serialized_start=1629
  _DATAPLEXZONE._serialized_end=2369
  _DATAPLEXZONE_ASSETSTATUSENTRY._serialized_start=832
  _DATAPLEXZONE_ASSETSTATUSENTRY._serialized_end=882
  _DATAPLEXZONE_LABELSENTRY._serialized_start=884
  _DATAPLEXZONE_LABELSENTRY._serialized_end=929
# @@protoc_insertion_point(module_scope)
