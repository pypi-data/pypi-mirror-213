# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: azure/azure_microsoft_network_loadbalancers.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1azure/azure_microsoft_network_loadbalancers.proto\x12\x31oak9.tython.azure.microsoft_network_loadbalancers\x1a\x13shared/shared.proto\"\xfa\x02\n\x1fMicrosoft_Network_loadBalancers\x12X\n\x0eload_balancers\x18\x01 \x01(\x0b\x32@.oak9.tython.azure.microsoft_network_loadbalancers.LoadBalancers\x12\x81\x01\n$load_balancers_backend_address_pools\x18\x02 \x03(\x0b\x32S.oak9.tython.azure.microsoft_network_loadbalancers.LoadBalancersBackendAddressPools\x12y\n load_balancers_inbound_nat_rules\x18\x03 \x03(\x0b\x32O.oak9.tython.azure.microsoft_network_loadbalancers.LoadBalancersInboundNatRules\"\x9e\x02\n\x1cLoadBalancersInboundNatRules\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12!\n\x19\x66rontend_ip_configuration\x18\x03 \x01(\t\x12\x10\n\x08protocol\x18\x04 \x01(\t\x12\x15\n\rfrontend_port\x18\x05 \x01(\x05\x12\x14\n\x0c\x62\x61\x63kend_port\x18\x06 \x01(\x05\x12\x1f\n\x17idle_timeout_in_minutes\x18\x07 \x01(\x05\x12\x1a\n\x12\x65nable_floating_ip\x18\x08 \x01(\x08\x12\x18\n\x10\x65nable_tcp_reset\x18\t \x01(\x08\"\xf3\x01\n LoadBalancersBackendAddressPools\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08location\x18\x03 \x01(\t\x12v\n\x1fload_balancer_backend_addresses\x18\x04 \x03(\x0b\x32M.oak9.tython.azure.microsoft_network_loadbalancers.LoadBalancerBackendAddress\"\xb9\x08\n\rLoadBalancers\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08location\x18\x03 \x01(\t\x12X\n\x04tags\x18\x04 \x03(\x0b\x32J.oak9.tython.azure.microsoft_network_loadbalancers.LoadBalancers.TagsEntry\x12^\n\x11\x65xtended_location\x18\x05 \x01(\x0b\x32\x43.oak9.tython.azure.microsoft_network_loadbalancers.ExtendedLocation\x12O\n\x03sku\x18\x06 \x01(\x0b\x32\x42.oak9.tython.azure.microsoft_network_loadbalancers.LoadBalancerSku\x12n\n\x1a\x66rontend_ip_configurations\x18\x07 \x03(\x0b\x32J.oak9.tython.azure.microsoft_network_loadbalancers.FrontendIPConfiguration\x12\x64\n\x15\x62\x61\x63kend_address_pools\x18\x08 \x03(\x0b\x32\x45.oak9.tython.azure.microsoft_network_loadbalancers.BackendAddressPool\x12\x62\n\x14load_balancing_rules\x18\t \x03(\x0b\x32\x44.oak9.tython.azure.microsoft_network_loadbalancers.LoadBalancingRule\x12H\n\x06probes\x18\n \x03(\x0b\x32\x38.oak9.tython.azure.microsoft_network_loadbalancers.Probe\x12\\\n\x11inbound_nat_rules\x18\x0b \x03(\x0b\x32\x41.oak9.tython.azure.microsoft_network_loadbalancers.InboundNatRule\x12\\\n\x11inbound_nat_pools\x18\x0c \x03(\x0b\x32\x41.oak9.tython.azure.microsoft_network_loadbalancers.InboundNatPool\x12W\n\x0eoutbound_rules\x18\r \x03(\x0b\x32?.oak9.tython.azure.microsoft_network_loadbalancers.OutboundRule\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xcd\x01\n\x0cOutboundRule\x12 \n\x18\x61llocated_outbound_ports\x18\x01 \x01(\x05\x12\"\n\x1a\x66rontend_ip_configurations\x18\x02 \x03(\t\x12\x1c\n\x14\x62\x61\x63kend_address_pool\x18\x03 \x01(\t\x12\x10\n\x08protocol\x18\x04 \x01(\t\x12\x18\n\x10\x65nable_tcp_reset\x18\x05 \x01(\x08\x12\x1f\n\x17idle_timeout_in_minutes\x18\x06 \x01(\x05\x12\x0c\n\x04name\x18\x07 \x01(\t\"\x84\x02\n\x0eInboundNatPool\x12!\n\x19\x66rontend_ip_configuration\x18\x01 \x01(\t\x12\x10\n\x08protocol\x18\x02 \x01(\t\x12!\n\x19\x66rontend_port_range_start\x18\x03 \x01(\x05\x12\x1f\n\x17\x66rontend_port_range_end\x18\x04 \x01(\x05\x12\x14\n\x0c\x62\x61\x63kend_port\x18\x05 \x01(\x05\x12\x1f\n\x17idle_timeout_in_minutes\x18\x06 \x01(\x05\x12\x1a\n\x12\x65nable_floating_ip\x18\x07 \x01(\x08\x12\x18\n\x10\x65nable_tcp_reset\x18\x08 \x01(\x08\x12\x0c\n\x04name\x18\t \x01(\t\"\xd7\x01\n\x0eInboundNatRule\x12!\n\x19\x66rontend_ip_configuration\x18\x01 \x01(\t\x12\x10\n\x08protocol\x18\x02 \x01(\t\x12\x15\n\rfrontend_port\x18\x03 \x01(\x05\x12\x14\n\x0c\x62\x61\x63kend_port\x18\x04 \x01(\x05\x12\x1f\n\x17idle_timeout_in_minutes\x18\x05 \x01(\x05\x12\x1a\n\x12\x65nable_floating_ip\x18\x06 \x01(\x08\x12\x18\n\x10\x65nable_tcp_reset\x18\x07 \x01(\x08\x12\x0c\n\x04name\x18\x08 \x01(\t\"\x82\x01\n\x05Probe\x12\x10\n\x08protocol\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\x12\x1b\n\x13interval_in_seconds\x18\x03 \x01(\x05\x12\x18\n\x10number_of_probes\x18\x04 \x01(\x05\x12\x14\n\x0crequest_path\x18\x05 \x01(\t\x12\x0c\n\x04name\x18\x06 \x01(\t\"\xc1\x02\n\x11LoadBalancingRule\x12!\n\x19\x66rontend_ip_configuration\x18\x01 \x01(\t\x12\x1c\n\x14\x62\x61\x63kend_address_pool\x18\x02 \x01(\t\x12\r\n\x05probe\x18\x03 \x01(\t\x12\x10\n\x08protocol\x18\x04 \x01(\t\x12\x19\n\x11load_distribution\x18\x05 \x01(\t\x12\x15\n\rfrontend_port\x18\x06 \x01(\x05\x12\x14\n\x0c\x62\x61\x63kend_port\x18\x07 \x01(\x05\x12\x1f\n\x17idle_timeout_in_minutes\x18\x08 \x01(\x05\x12\x1a\n\x12\x65nable_floating_ip\x18\t \x01(\x08\x12\x18\n\x10\x65nable_tcp_reset\x18\n \x01(\x08\x12\x1d\n\x15\x64isable_outbound_snat\x18\x0b \x01(\x08\x12\x0c\n\x04name\x18\x0c \x01(\t\"\xac\x01\n\x12\x42\x61\x63kendAddressPool\x12\x10\n\x08location\x18\x01 \x01(\t\x12v\n\x1fload_balancer_backend_addresses\x18\x02 \x03(\x0b\x32M.oak9.tython.azure.microsoft_network_loadbalancers.LoadBalancerBackendAddress\x12\x0c\n\x04name\x18\x03 \x01(\t\"\x88\x01\n\x1aLoadBalancerBackendAddress\x12\x17\n\x0fvirtual_network\x18\x01 \x01(\t\x12\x12\n\nip_address\x18\x02 \x01(\t\x12/\n\'load_balancer_frontend_ip_configuration\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\"\xe1\x01\n\x17\x46rontendIPConfiguration\x12\x1a\n\x12private_ip_address\x18\x01 \x01(\t\x12$\n\x1cprivate_ip_allocation_method\x18\x02 \x01(\t\x12\"\n\x1aprivate_ip_address_version\x18\x03 \x01(\t\x12\x0e\n\x06subnet\x18\x04 \x01(\t\x12\x19\n\x11public_ip_address\x18\x05 \x01(\t\x12\x18\n\x10public_ip_prefix\x18\x06 \x01(\t\x12\x0c\n\x04name\x18\x07 \x01(\t\x12\r\n\x05zones\x18\x08 \x03(\t\"-\n\x0fLoadBalancerSku\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04tier\x18\x02 \x01(\t\".\n\x10\x45xtendedLocation\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'azure.azure_microsoft_network_loadbalancers_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _LOADBALANCERS_TAGSENTRY._options = None
  _LOADBALANCERS_TAGSENTRY._serialized_options = b'8\001'
  _MICROSOFT_NETWORK_LOADBALANCERS._serialized_start=126
  _MICROSOFT_NETWORK_LOADBALANCERS._serialized_end=504
  _LOADBALANCERSINBOUNDNATRULES._serialized_start=507
  _LOADBALANCERSINBOUNDNATRULES._serialized_end=793
  _LOADBALANCERSBACKENDADDRESSPOOLS._serialized_start=796
  _LOADBALANCERSBACKENDADDRESSPOOLS._serialized_end=1039
  _LOADBALANCERS._serialized_start=1042
  _LOADBALANCERS._serialized_end=2123
  _LOADBALANCERS_TAGSENTRY._serialized_start=2080
  _LOADBALANCERS_TAGSENTRY._serialized_end=2123
  _OUTBOUNDRULE._serialized_start=2126
  _OUTBOUNDRULE._serialized_end=2331
  _INBOUNDNATPOOL._serialized_start=2334
  _INBOUNDNATPOOL._serialized_end=2594
  _INBOUNDNATRULE._serialized_start=2597
  _INBOUNDNATRULE._serialized_end=2812
  _PROBE._serialized_start=2815
  _PROBE._serialized_end=2945
  _LOADBALANCINGRULE._serialized_start=2948
  _LOADBALANCINGRULE._serialized_end=3269
  _BACKENDADDRESSPOOL._serialized_start=3272
  _BACKENDADDRESSPOOL._serialized_end=3444
  _LOADBALANCERBACKENDADDRESS._serialized_start=3447
  _LOADBALANCERBACKENDADDRESS._serialized_end=3583
  _FRONTENDIPCONFIGURATION._serialized_start=3586
  _FRONTENDIPCONFIGURATION._serialized_end=3811
  _LOADBALANCERSKU._serialized_start=3813
  _LOADBALANCERSKU._serialized_end=3858
  _EXTENDEDLOCATION._serialized_start=3860
  _EXTENDEDLOCATION._serialized_end=3906
# @@protoc_insertion_point(module_scope)
