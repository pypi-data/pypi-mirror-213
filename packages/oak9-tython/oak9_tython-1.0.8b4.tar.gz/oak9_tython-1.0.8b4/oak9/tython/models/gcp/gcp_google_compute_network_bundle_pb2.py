# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gcp/gcp_google_compute_network_bundle.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2
from oak9.tython.models.gcp import gcp_compute_network_pb2 as gcp_dot_gcp__compute__network__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+gcp/gcp_google_compute_network_bundle.proto\x12-oak9.tython.gcp.google_compute_network_bundle\x1a\x13shared/shared.proto\x1a\x1dgcp/gcp_compute_network.proto\"\xac\x02\n\x14GoogleComputeNetwork\x12H\n\x0f\x63ompute_network\x18\x01 \x01(\x0b\x32/.oak9.tython.gcp.compute_network.ComputeNetwork\x12W\n\x17\x63ompute_network_peering\x18\x02 \x03(\x0b\x32\x36.oak9.tython.gcp.compute_network.ComputeNetworkPeering\x12q\n%compute_network_peering_routes_config\x18\x03 \x03(\x0b\x32\x42.oak9.tython.gcp.compute_network.ComputeNetworkPeeringRoutesConfigb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gcp.gcp_google_compute_network_bundle_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GOOGLECOMPUTENETWORK._serialized_start=147
  _GOOGLECOMPUTENETWORK._serialized_end=447
# @@protoc_insertion_point(module_scope)
