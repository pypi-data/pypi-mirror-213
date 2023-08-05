# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: azure/azure_microsoft_sql.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1f\x61zure/azure_microsoft_sql.proto\x12\x1foak9.tython.azure.microsoft_sql\x1a\x13shared/shared.proto\"\xa9\x02\n\rMicrosoft_Sql\x12\x46\n\x0einstance_pools\x18\x01 \x03(\x0b\x32..oak9.tython.azure.microsoft_sql.InstancePools\x12l\n\"locations_instance_failover_groups\x18\x02 \x03(\x0b\x32@.oak9.tython.azure.microsoft_sql.LocationsInstanceFailoverGroups\x12\x62\n\x1dlocations_server_trust_groups\x18\x03 \x03(\x0b\x32;.oak9.tython.azure.microsoft_sql.LocationsServerTrustGroups\"\xbd\x01\n\x1aLocationsServerTrustGroups\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x42\n\rgroup_members\x18\x03 \x03(\x0b\x32+.oak9.tython.azure.microsoft_sql.ServerInfo\x12\x14\n\x0ctrust_scopes\x18\x04 \x03(\t\"\x1f\n\nServerInfo\x12\x11\n\tserver_id\x18\x01 \x01(\t\"\xd9\x03\n\x1fLocationsInstanceFailoverGroups\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12X\n\x16managed_instance_pairs\x18\x03 \x03(\x0b\x32\x38.oak9.tython.azure.microsoft_sql.ManagedInstancePairInfo\x12K\n\x0fpartner_regions\x18\x04 \x03(\x0b\x32\x32.oak9.tython.azure.microsoft_sql.PartnerRegionInfo\x12\x62\n\x12read_only_endpoint\x18\x05 \x01(\x0b\x32\x46.oak9.tython.azure.microsoft_sql.InstanceFailoverGroupReadOnlyEndpoint\x12\x64\n\x13read_write_endpoint\x18\x06 \x01(\x0b\x32G.oak9.tython.azure.microsoft_sql.InstanceFailoverGroupReadWriteEndpoint\"w\n&InstanceFailoverGroupReadWriteEndpoint\x12\x17\n\x0f\x66\x61ilover_policy\x18\x01 \x01(\t\x12\x34\n,failover_with_data_loss_grace_period_minutes\x18\x02 \x01(\x05\"@\n%InstanceFailoverGroupReadOnlyEndpoint\x12\x17\n\x0f\x66\x61ilover_policy\x18\x01 \x01(\t\"%\n\x11PartnerRegionInfo\x12\x10\n\x08location\x18\x01 \x01(\t\"c\n\x17ManagedInstancePairInfo\x12#\n\x1bpartner_managed_instance_id\x18\x01 \x01(\t\x12#\n\x1bprimary_managed_instance_id\x18\x02 \x01(\t\"\xca\x02\n\rInstancePools\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x10\n\x08location\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x14\n\x0clicense_type\x18\x04 \x01(\t\x12\x11\n\tsubnet_id\x18\x05 \x01(\t\x12\x0f\n\x07v_cores\x18\x06 \x01(\x05\x12\x31\n\x03sku\x18\x07 \x01(\x0b\x32$.oak9.tython.azure.microsoft_sql.Sku\x12\x46\n\x04tags\x18\x08 \x03(\x0b\x32\x38.oak9.tython.azure.microsoft_sql.InstancePools.TagsEntry\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"Q\n\x03Sku\x12\x10\n\x08\x63\x61pacity\x18\x01 \x01(\x05\x12\x0e\n\x06\x66\x61mily\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0c\n\x04size\x18\x04 \x01(\t\x12\x0c\n\x04tier\x18\x05 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'azure.azure_microsoft_sql_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _INSTANCEPOOLS_TAGSENTRY._options = None
  _INSTANCEPOOLS_TAGSENTRY._serialized_options = b'8\001'
  _MICROSOFT_SQL._serialized_start=90
  _MICROSOFT_SQL._serialized_end=387
  _LOCATIONSSERVERTRUSTGROUPS._serialized_start=390
  _LOCATIONSSERVERTRUSTGROUPS._serialized_end=579
  _SERVERINFO._serialized_start=581
  _SERVERINFO._serialized_end=612
  _LOCATIONSINSTANCEFAILOVERGROUPS._serialized_start=615
  _LOCATIONSINSTANCEFAILOVERGROUPS._serialized_end=1088
  _INSTANCEFAILOVERGROUPREADWRITEENDPOINT._serialized_start=1090
  _INSTANCEFAILOVERGROUPREADWRITEENDPOINT._serialized_end=1209
  _INSTANCEFAILOVERGROUPREADONLYENDPOINT._serialized_start=1211
  _INSTANCEFAILOVERGROUPREADONLYENDPOINT._serialized_end=1275
  _PARTNERREGIONINFO._serialized_start=1277
  _PARTNERREGIONINFO._serialized_end=1314
  _MANAGEDINSTANCEPAIRINFO._serialized_start=1316
  _MANAGEDINSTANCEPAIRINFO._serialized_end=1415
  _INSTANCEPOOLS._serialized_start=1418
  _INSTANCEPOOLS._serialized_end=1748
  _INSTANCEPOOLS_TAGSENTRY._serialized_start=1705
  _INSTANCEPOOLS_TAGSENTRY._serialized_end=1748
  _SKU._serialized_start=1750
  _SKU._serialized_end=1831
# @@protoc_insertion_point(module_scope)
