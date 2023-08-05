# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: kubernetes/kubernetes_io.k8s.api.flowcontrol.v1beta2.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2
from oak9.tython.models.kubernetes.kubernetes_io.k8s.apimachinery.pkg.apis.meta import v1_pb2 as kubernetes_dot_kubernetes__io_dot_k8s_dot_apimachinery_dot_pkg_dot_apis_dot_meta_dot_v1__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n:kubernetes/kubernetes_io.k8s.api.flowcontrol.v1beta2.proto\x12\'oak9.tython.k8s.api.flowcontrol.v1beta2\x1a\x13shared/shared.proto\x1a@kubernetes/kubernetes_io.k8s.apimachinery.pkg.apis.meta.v1.proto\"`\n\x17\x46lowDistinguisherMethod\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x37\n\rresource_info\x18\x02 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xc7\x02\n\nFlowSchema\x12\x13\n\x0b\x61pi_version\x18\x01 \x01(\t\x12\x0c\n\x04kind\x18\x02 \x01(\t\x12K\n\x08metadata\x18\x03 \x01(\x0b\x32\x39.oak9.tython.k8s.apimachinery.pkg.apis.meta.v1.ObjectMeta\x12\x45\n\x04spec\x18\x04 \x01(\x0b\x32\x37.oak9.tython.k8s.api.flowcontrol.v1beta2.FlowSchemaSpec\x12I\n\x06status\x18\x05 \x01(\x0b\x32\x39.oak9.tython.k8s.api.flowcontrol.v1beta2.FlowSchemaStatus\x12\x37\n\rresource_info\x18\x06 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xe0\x01\n\x13\x46lowSchemaCondition\x12Q\n\x14last_transition_time\x18\x01 \x01(\x0b\x32\x33.oak9.tython.k8s.apimachinery.pkg.apis.meta.v1.Time\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x0e\n\x06reason\x18\x03 \x01(\t\x12\x0e\n\x06status\x18\x04 \x01(\t\x12\x0c\n\x04type\x18\x05 \x01(\t\x12\x37\n\rresource_info\x18\x06 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xfb\x01\n\x0e\x46lowSchemaList\x12\x13\n\x0b\x61pi_version\x18\x01 \x01(\t\x12\x42\n\x05items\x18\x02 \x03(\x0b\x32\x33.oak9.tython.k8s.api.flowcontrol.v1beta2.FlowSchema\x12\x0c\n\x04kind\x18\x03 \x01(\t\x12I\n\x08metadata\x18\x04 \x01(\x0b\x32\x37.oak9.tython.k8s.apimachinery.pkg.apis.meta.v1.ListMeta\x12\x37\n\rresource_info\x18\x05 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\x8b\x03\n\x0e\x46lowSchemaSpec\x12^\n\x14\x64istinguisher_method\x18\x01 \x01(\x0b\x32@.oak9.tython.k8s.api.flowcontrol.v1beta2.FlowDistinguisherMethod\x12\x1b\n\x13matching_precedence\x18\x02 \x01(\x05\x12r\n\x1cpriority_level_configuration\x18\x03 \x01(\x0b\x32L.oak9.tython.k8s.api.flowcontrol.v1beta2.PriorityLevelConfigurationReference\x12O\n\x05rules\x18\x04 \x03(\x0b\x32@.oak9.tython.k8s.api.flowcontrol.v1beta2.PolicyRulesWithSubjects\x12\x37\n\rresource_info\x18\x05 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\x9d\x01\n\x10\x46lowSchemaStatus\x12P\n\nconditions\x18\x01 \x03(\x0b\x32<.oak9.tython.k8s.api.flowcontrol.v1beta2.FlowSchemaCondition\x12\x37\n\rresource_info\x18\x02 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"U\n\x0cGroupSubject\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x37\n\rresource_info\x18\x02 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xa6\x01\n\rLimitResponse\x12N\n\x07queuing\x18\x01 \x01(\x0b\x32=.oak9.tython.k8s.api.flowcontrol.v1beta2.QueuingConfiguration\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x37\n\rresource_info\x18\x03 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\x8b\x02\n!LimitedPriorityLevelConfiguration\x12\"\n\x1a\x61ssured_concurrency_shares\x18\x01 \x01(\x05\x12\x1f\n\x17\x62orrowing_limit_percent\x18\x02 \x01(\x05\x12\x18\n\x10lendable_percent\x18\x03 \x01(\x05\x12N\n\x0elimit_response\x18\x04 \x01(\x0b\x32\x36.oak9.tython.k8s.api.flowcontrol.v1beta2.LimitResponse\x12\x37\n\rresource_info\x18\x05 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"|\n\x15NonResourcePolicyRule\x12\x1b\n\x13non_resource_u_r_ls\x18\x01 \x03(\t\x12\r\n\x05verbs\x18\x02 \x03(\t\x12\x37\n\rresource_info\x18\x03 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xc7\x02\n\x17PolicyRulesWithSubjects\x12Z\n\x12non_resource_rules\x18\x01 \x03(\x0b\x32>.oak9.tython.k8s.api.flowcontrol.v1beta2.NonResourcePolicyRule\x12S\n\x0eresource_rules\x18\x02 \x03(\x0b\x32;.oak9.tython.k8s.api.flowcontrol.v1beta2.ResourcePolicyRule\x12\x42\n\x08subjects\x18\x03 \x03(\x0b\x32\x30.oak9.tython.k8s.api.flowcontrol.v1beta2.Subject\x12\x37\n\rresource_info\x18\x04 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xf7\x02\n\x1aPriorityLevelConfiguration\x12\x13\n\x0b\x61pi_version\x18\x01 \x01(\t\x12\x0c\n\x04kind\x18\x02 \x01(\t\x12K\n\x08metadata\x18\x03 \x01(\x0b\x32\x39.oak9.tython.k8s.apimachinery.pkg.apis.meta.v1.ObjectMeta\x12U\n\x04spec\x18\x04 \x01(\x0b\x32G.oak9.tython.k8s.api.flowcontrol.v1beta2.PriorityLevelConfigurationSpec\x12Y\n\x06status\x18\x05 \x01(\x0b\x32I.oak9.tython.k8s.api.flowcontrol.v1beta2.PriorityLevelConfigurationStatus\x12\x37\n\rresource_info\x18\x06 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xf0\x01\n#PriorityLevelConfigurationCondition\x12Q\n\x14last_transition_time\x18\x01 \x01(\x0b\x32\x33.oak9.tython.k8s.apimachinery.pkg.apis.meta.v1.Time\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x0e\n\x06reason\x18\x03 \x01(\t\x12\x0e\n\x06status\x18\x04 \x01(\t\x12\x0c\n\x04type\x18\x05 \x01(\t\x12\x37\n\rresource_info\x18\x06 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\x9b\x02\n\x1ePriorityLevelConfigurationList\x12\x13\n\x0b\x61pi_version\x18\x01 \x01(\t\x12R\n\x05items\x18\x02 \x03(\x0b\x32\x43.oak9.tython.k8s.api.flowcontrol.v1beta2.PriorityLevelConfiguration\x12\x0c\n\x04kind\x18\x03 \x01(\t\x12I\n\x08metadata\x18\x04 \x01(\x0b\x32\x37.oak9.tython.k8s.apimachinery.pkg.apis.meta.v1.ListMeta\x12\x37\n\rresource_info\x18\x05 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"l\n#PriorityLevelConfigurationReference\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x37\n\rresource_info\x18\x02 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xc4\x01\n\x1ePriorityLevelConfigurationSpec\x12[\n\x07limited\x18\x01 \x01(\x0b\x32J.oak9.tython.k8s.api.flowcontrol.v1beta2.LimitedPriorityLevelConfiguration\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x37\n\rresource_info\x18\x03 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xbd\x01\n PriorityLevelConfigurationStatus\x12`\n\nconditions\x18\x01 \x03(\x0b\x32L.oak9.tython.k8s.api.flowcontrol.v1beta2.PriorityLevelConfigurationCondition\x12\x37\n\rresource_info\x18\x02 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\x8e\x01\n\x14QueuingConfiguration\x12\x11\n\thand_size\x18\x01 \x01(\x05\x12\x1a\n\x12queue_length_limit\x18\x02 \x01(\x05\x12\x0e\n\x06queues\x18\x03 \x01(\x05\x12\x37\n\rresource_info\x18\x04 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xae\x01\n\x12ResourcePolicyRule\x12\x12\n\napi_groups\x18\x01 \x03(\t\x12\x15\n\rcluster_scope\x18\x02 \x01(\x08\x12\x12\n\nnamespaces\x18\x03 \x03(\t\x12\x11\n\tresources\x18\x04 \x03(\t\x12\r\n\x05verbs\x18\x05 \x03(\t\x12\x37\n\rresource_info\x18\x06 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"q\n\x15ServiceAccountSubject\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\tnamespace\x18\x02 \x01(\t\x12\x37\n\rresource_info\x18\x03 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\xb3\x02\n\x07Subject\x12\x44\n\x05group\x18\x01 \x01(\x0b\x32\x35.oak9.tython.k8s.api.flowcontrol.v1beta2.GroupSubject\x12\x0c\n\x04kind\x18\x02 \x01(\t\x12W\n\x0fservice_account\x18\x03 \x01(\x0b\x32>.oak9.tython.k8s.api.flowcontrol.v1beta2.ServiceAccountSubject\x12\x42\n\x04user\x18\x04 \x01(\x0b\x32\x34.oak9.tython.k8s.api.flowcontrol.v1beta2.UserSubject\x12\x37\n\rresource_info\x18\x05 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"T\n\x0bUserSubject\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x37\n\rresource_info\x18\x02 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'kubernetes.kubernetes_io.k8s.api.flowcontrol.v1beta2_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _FLOWDISTINGUISHERMETHOD._serialized_start=190
  _FLOWDISTINGUISHERMETHOD._serialized_end=286
  _FLOWSCHEMA._serialized_start=289
  _FLOWSCHEMA._serialized_end=616
  _FLOWSCHEMACONDITION._serialized_start=619
  _FLOWSCHEMACONDITION._serialized_end=843
  _FLOWSCHEMALIST._serialized_start=846
  _FLOWSCHEMALIST._serialized_end=1097
  _FLOWSCHEMASPEC._serialized_start=1100
  _FLOWSCHEMASPEC._serialized_end=1495
  _FLOWSCHEMASTATUS._serialized_start=1498
  _FLOWSCHEMASTATUS._serialized_end=1655
  _GROUPSUBJECT._serialized_start=1657
  _GROUPSUBJECT._serialized_end=1742
  _LIMITRESPONSE._serialized_start=1745
  _LIMITRESPONSE._serialized_end=1911
  _LIMITEDPRIORITYLEVELCONFIGURATION._serialized_start=1914
  _LIMITEDPRIORITYLEVELCONFIGURATION._serialized_end=2181
  _NONRESOURCEPOLICYRULE._serialized_start=2183
  _NONRESOURCEPOLICYRULE._serialized_end=2307
  _POLICYRULESWITHSUBJECTS._serialized_start=2310
  _POLICYRULESWITHSUBJECTS._serialized_end=2637
  _PRIORITYLEVELCONFIGURATION._serialized_start=2640
  _PRIORITYLEVELCONFIGURATION._serialized_end=3015
  _PRIORITYLEVELCONFIGURATIONCONDITION._serialized_start=3018
  _PRIORITYLEVELCONFIGURATIONCONDITION._serialized_end=3258
  _PRIORITYLEVELCONFIGURATIONLIST._serialized_start=3261
  _PRIORITYLEVELCONFIGURATIONLIST._serialized_end=3544
  _PRIORITYLEVELCONFIGURATIONREFERENCE._serialized_start=3546
  _PRIORITYLEVELCONFIGURATIONREFERENCE._serialized_end=3654
  _PRIORITYLEVELCONFIGURATIONSPEC._serialized_start=3657
  _PRIORITYLEVELCONFIGURATIONSPEC._serialized_end=3853
  _PRIORITYLEVELCONFIGURATIONSTATUS._serialized_start=3856
  _PRIORITYLEVELCONFIGURATIONSTATUS._serialized_end=4045
  _QUEUINGCONFIGURATION._serialized_start=4048
  _QUEUINGCONFIGURATION._serialized_end=4190
  _RESOURCEPOLICYRULE._serialized_start=4193
  _RESOURCEPOLICYRULE._serialized_end=4367
  _SERVICEACCOUNTSUBJECT._serialized_start=4369
  _SERVICEACCOUNTSUBJECT._serialized_end=4482
  _SUBJECT._serialized_start=4485
  _SUBJECT._serialized_end=4792
  _USERSUBJECT._serialized_start=4794
  _USERSUBJECT._serialized_end=4878
# @@protoc_insertion_point(module_scope)
