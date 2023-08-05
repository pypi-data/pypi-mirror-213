# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gcp/gcp_dns.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11gcp/gcp_dns.proto\x12\x13oak9.tython.gcp.dns\x1a\x13shared/shared.proto\"t\n+DnsManagedZoneXDnssecConfigXDefaultKeySpecs\x12\x11\n\talgorithm\x18\x01 \x01(\t\x12\x12\n\nkey_length\x18\x02 \x01(\x01\x12\x10\n\x08key_type\x18\x03 \x01(\t\x12\x0c\n\x04kind\x18\x04 \x01(\t\"\xae\x01\n\x1b\x44nsManagedZoneXDnssecConfig\x12\x0c\n\x04kind\x18\x01 \x01(\t\x12\x15\n\rnon_existence\x18\x02 \x01(\t\x12\r\n\x05state\x18\x03 \x01(\t\x12[\n\x11\x64\x65\x66\x61ult_key_specs\x18\x04 \x03(\x0b\x32@.oak9.tython.gcp.dns.DnsManagedZoneXDnssecConfigXDefaultKeySpecs\"b\n1DnsManagedZoneXForwardingConfigXTargetNameServers\x12\x17\n\x0f\x66orwarding_path\x18\x01 \x01(\t\x12\x14\n\x0cipv4_address\x18\x02 \x01(\t\"\x86\x01\n\x1f\x44nsManagedZoneXForwardingConfig\x12\x63\n\x13target_name_servers\x18\x01 \x03(\x0b\x32\x46.oak9.tython.gcp.dns.DnsManagedZoneXForwardingConfigXTargetNameServers\"A\n*DnsManagedZoneXPeeringConfigXTargetNetwork\x12\x13\n\x0bnetwork_url\x18\x01 \x01(\t\"w\n\x1c\x44nsManagedZoneXPeeringConfig\x12W\n\x0etarget_network\x18\x01 \x01(\x0b\x32?.oak9.tython.gcp.dns.DnsManagedZoneXPeeringConfigXTargetNetwork\"F\n/DnsManagedZoneXPrivateVisibilityConfigXNetworks\x12\x13\n\x0bnetwork_url\x18\x01 \x01(\t\"\x80\x01\n&DnsManagedZoneXPrivateVisibilityConfig\x12V\n\x08networks\x18\x01 \x03(\x0b\x32\x44.oak9.tython.gcp.dns.DnsManagedZoneXPrivateVisibilityConfigXNetworks\"I\n\x17\x44nsManagedZoneXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\x12\x0e\n\x06update\x18\x03 \x01(\t\"\x81\x06\n\x0e\x44nsManagedZone\x12\x15\n\rcreation_time\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x10\n\x08\x64ns_name\x18\x03 \x01(\t\x12\x15\n\rforce_destroy\x18\x04 \x01(\x08\x12\n\n\x02id\x18\x05 \x01(\t\x12?\n\x06labels\x18\x06 \x03(\x0b\x32/.oak9.tython.gcp.dns.DnsManagedZone.LabelsEntry\x12\x17\n\x0fmanaged_zone_id\x18\x07 \x01(\x01\x12\x0c\n\x04name\x18\x08 \x01(\t\x12\x14\n\x0cname_servers\x18\t \x03(\t\x12\x0f\n\x07project\x18\n \x01(\t\x12\x12\n\nvisibility\x18\x0b \x01(\t\x12G\n\rdnssec_config\x18\x0c \x01(\x0b\x32\x30.oak9.tython.gcp.dns.DnsManagedZoneXDnssecConfig\x12O\n\x11\x66orwarding_config\x18\r \x01(\x0b\x32\x34.oak9.tython.gcp.dns.DnsManagedZoneXForwardingConfig\x12I\n\x0epeering_config\x18\x0e \x01(\x0b\x32\x31.oak9.tython.gcp.dns.DnsManagedZoneXPeeringConfig\x12^\n\x19private_visibility_config\x18\x0f \x01(\x0b\x32;.oak9.tython.gcp.dns.DnsManagedZoneXPrivateVisibilityConfig\x12>\n\x08timeouts\x18\x10 \x01(\x0b\x32,.oak9.tython.gcp.dns.DnsManagedZoneXTimeouts\x12\x37\n\rresource_info\x18\x11 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"h\n7DnsPolicyXAlternativeNameServerConfigXTargetNameServers\x12\x17\n\x0f\x66orwarding_path\x18\x01 \x01(\t\x12\x14\n\x0cipv4_address\x18\x02 \x01(\t\"\x92\x01\n%DnsPolicyXAlternativeNameServerConfig\x12i\n\x13target_name_servers\x18\x01 \x03(\x0b\x32L.oak9.tython.gcp.dns.DnsPolicyXAlternativeNameServerConfigXTargetNameServers\")\n\x12\x44nsPolicyXNetworks\x12\x13\n\x0bnetwork_url\x18\x01 \x01(\t\"D\n\x12\x44nsPolicyXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\x12\x0e\n\x06update\x18\x03 \x01(\t\"\x99\x03\n\tDnsPolicy\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12!\n\x19\x65nable_inbound_forwarding\x18\x02 \x01(\x08\x12\x16\n\x0e\x65nable_logging\x18\x03 \x01(\x08\x12\n\n\x02id\x18\x04 \x01(\t\x12\x0c\n\x04name\x18\x05 \x01(\t\x12\x0f\n\x07project\x18\x06 \x01(\t\x12\x62\n\x1e\x61lternative_name_server_config\x18\x07 \x01(\x0b\x32:.oak9.tython.gcp.dns.DnsPolicyXAlternativeNameServerConfig\x12\x39\n\x08networks\x18\x08 \x03(\x0b\x32\'.oak9.tython.gcp.dns.DnsPolicyXNetworks\x12\x39\n\x08timeouts\x18\t \x01(\x0b\x32\'.oak9.tython.gcp.dns.DnsPolicyXTimeouts\x12\x37\n\rresource_info\x18\n \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"C\n\x1e\x44nsRecordSetXRoutingPolicyXGeo\x12\x10\n\x08location\x18\x01 \x01(\t\x12\x0f\n\x07rrdatas\x18\x02 \x03(\t\"A\n\x1e\x44nsRecordSetXRoutingPolicyXWrr\x12\x0f\n\x07rrdatas\x18\x01 \x03(\t\x12\x0e\n\x06weight\x18\x02 \x01(\x01\"\xa0\x01\n\x1a\x44nsRecordSetXRoutingPolicy\x12@\n\x03geo\x18\x01 \x03(\x0b\x32\x33.oak9.tython.gcp.dns.DnsRecordSetXRoutingPolicyXGeo\x12@\n\x03wrr\x18\x02 \x03(\x0b\x32\x33.oak9.tython.gcp.dns.DnsRecordSetXRoutingPolicyXWrr\"\xfd\x01\n\x0c\x44nsRecordSet\x12\n\n\x02id\x18\x01 \x01(\t\x12\x14\n\x0cmanaged_zone\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0f\n\x07project\x18\x04 \x01(\t\x12\x0f\n\x07rrdatas\x18\x05 \x03(\t\x12\x0b\n\x03ttl\x18\x06 \x01(\x01\x12\x0c\n\x04type\x18\x07 \x01(\t\x12G\n\x0erouting_policy\x18\x08 \x01(\x0b\x32/.oak9.tython.gcp.dns.DnsRecordSetXRoutingPolicy\x12\x37\n\rresource_info\x18\t \x01(\x0b\x32 .oak9.tython.shared.ResourceInfob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gcp.gcp_dns_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _DNSMANAGEDZONE_LABELSENTRY._options = None
  _DNSMANAGEDZONE_LABELSENTRY._serialized_options = b'8\001'
  _DNSMANAGEDZONEXDNSSECCONFIGXDEFAULTKEYSPECS._serialized_start=63
  _DNSMANAGEDZONEXDNSSECCONFIGXDEFAULTKEYSPECS._serialized_end=179
  _DNSMANAGEDZONEXDNSSECCONFIG._serialized_start=182
  _DNSMANAGEDZONEXDNSSECCONFIG._serialized_end=356
  _DNSMANAGEDZONEXFORWARDINGCONFIGXTARGETNAMESERVERS._serialized_start=358
  _DNSMANAGEDZONEXFORWARDINGCONFIGXTARGETNAMESERVERS._serialized_end=456
  _DNSMANAGEDZONEXFORWARDINGCONFIG._serialized_start=459
  _DNSMANAGEDZONEXFORWARDINGCONFIG._serialized_end=593
  _DNSMANAGEDZONEXPEERINGCONFIGXTARGETNETWORK._serialized_start=595
  _DNSMANAGEDZONEXPEERINGCONFIGXTARGETNETWORK._serialized_end=660
  _DNSMANAGEDZONEXPEERINGCONFIG._serialized_start=662
  _DNSMANAGEDZONEXPEERINGCONFIG._serialized_end=781
  _DNSMANAGEDZONEXPRIVATEVISIBILITYCONFIGXNETWORKS._serialized_start=783
  _DNSMANAGEDZONEXPRIVATEVISIBILITYCONFIGXNETWORKS._serialized_end=853
  _DNSMANAGEDZONEXPRIVATEVISIBILITYCONFIG._serialized_start=856
  _DNSMANAGEDZONEXPRIVATEVISIBILITYCONFIG._serialized_end=984
  _DNSMANAGEDZONEXTIMEOUTS._serialized_start=986
  _DNSMANAGEDZONEXTIMEOUTS._serialized_end=1059
  _DNSMANAGEDZONE._serialized_start=1062
  _DNSMANAGEDZONE._serialized_end=1831
  _DNSMANAGEDZONE_LABELSENTRY._serialized_start=1786
  _DNSMANAGEDZONE_LABELSENTRY._serialized_end=1831
  _DNSPOLICYXALTERNATIVENAMESERVERCONFIGXTARGETNAMESERVERS._serialized_start=1833
  _DNSPOLICYXALTERNATIVENAMESERVERCONFIGXTARGETNAMESERVERS._serialized_end=1937
  _DNSPOLICYXALTERNATIVENAMESERVERCONFIG._serialized_start=1940
  _DNSPOLICYXALTERNATIVENAMESERVERCONFIG._serialized_end=2086
  _DNSPOLICYXNETWORKS._serialized_start=2088
  _DNSPOLICYXNETWORKS._serialized_end=2129
  _DNSPOLICYXTIMEOUTS._serialized_start=2131
  _DNSPOLICYXTIMEOUTS._serialized_end=2199
  _DNSPOLICY._serialized_start=2202
  _DNSPOLICY._serialized_end=2611
  _DNSRECORDSETXROUTINGPOLICYXGEO._serialized_start=2613
  _DNSRECORDSETXROUTINGPOLICYXGEO._serialized_end=2680
  _DNSRECORDSETXROUTINGPOLICYXWRR._serialized_start=2682
  _DNSRECORDSETXROUTINGPOLICYXWRR._serialized_end=2747
  _DNSRECORDSETXROUTINGPOLICY._serialized_start=2750
  _DNSRECORDSETXROUTINGPOLICY._serialized_end=2910
  _DNSRECORDSET._serialized_start=2913
  _DNSRECORDSET._serialized_end=3166
# @@protoc_insertion_point(module_scope)
