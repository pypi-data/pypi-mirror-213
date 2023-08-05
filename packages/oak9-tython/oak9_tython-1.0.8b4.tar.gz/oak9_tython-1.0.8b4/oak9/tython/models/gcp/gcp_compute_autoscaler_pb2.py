# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gcp/gcp_compute_autoscaler.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n gcp/gcp_compute_autoscaler.proto\x12\"oak9.tython.gcp.compute_autoscaler\x1a\x13shared/shared.proto\"_\n2ComputeAutoscalerXAutoscalingPolicyXCpuUtilization\x12\x19\n\x11predictive_method\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\x01\"N\n<ComputeAutoscalerXAutoscalingPolicyXLoadBalancingUtilization\x12\x0e\n\x06target\x18\x01 \x01(\x01\"X\n*ComputeAutoscalerXAutoscalingPolicyXMetric\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\x01\x12\x0c\n\x04type\x18\x03 \x01(\t\"h\nFComputeAutoscalerXAutoscalingPolicyXScaleInControlXMaxScaledInReplicas\x12\r\n\x05\x66ixed\x18\x01 \x01(\x01\x12\x0f\n\x07percent\x18\x02 \x01(\x01\"\xda\x01\n2ComputeAutoscalerXAutoscalingPolicyXScaleInControl\x12\x17\n\x0ftime_window_sec\x18\x01 \x01(\x01\x12\x8a\x01\n\x16max_scaled_in_replicas\x18\x02 \x01(\x0b\x32j.oak9.tython.gcp.compute_autoscaler.ComputeAutoscalerXAutoscalingPolicyXScaleInControlXMaxScaledInReplicas\"\xc5\x01\n4ComputeAutoscalerXAutoscalingPolicyXScalingSchedules\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12\x10\n\x08\x64isabled\x18\x02 \x01(\x08\x12\x14\n\x0c\x64uration_sec\x18\x03 \x01(\x01\x12\x1d\n\x15min_required_replicas\x18\x04 \x01(\x01\x12\x0c\n\x04name\x18\x05 \x01(\t\x12\x10\n\x08schedule\x18\x06 \x01(\t\x12\x11\n\ttime_zone\x18\x07 \x01(\t\"\xb7\x05\n#ComputeAutoscalerXAutoscalingPolicy\x12\x17\n\x0f\x63ooldown_period\x18\x01 \x01(\x01\x12\x14\n\x0cmax_replicas\x18\x02 \x01(\x01\x12\x14\n\x0cmin_replicas\x18\x03 \x01(\x01\x12\x0c\n\x04mode\x18\x04 \x01(\t\x12o\n\x0f\x63pu_utilization\x18\x05 \x01(\x0b\x32V.oak9.tython.gcp.compute_autoscaler.ComputeAutoscalerXAutoscalingPolicyXCpuUtilization\x12\x84\x01\n\x1aload_balancing_utilization\x18\x06 \x01(\x0b\x32`.oak9.tython.gcp.compute_autoscaler.ComputeAutoscalerXAutoscalingPolicyXLoadBalancingUtilization\x12^\n\x06metric\x18\x07 \x03(\x0b\x32N.oak9.tython.gcp.compute_autoscaler.ComputeAutoscalerXAutoscalingPolicyXMetric\x12p\n\x10scale_in_control\x18\x08 \x01(\x0b\x32V.oak9.tython.gcp.compute_autoscaler.ComputeAutoscalerXAutoscalingPolicyXScaleInControl\x12s\n\x11scaling_schedules\x18\t \x03(\x0b\x32X.oak9.tython.gcp.compute_autoscaler.ComputeAutoscalerXAutoscalingPolicyXScalingSchedules\"L\n\x1a\x43omputeAutoscalerXTimeouts\x12\x0e\n\x06\x63reate\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65lete\x18\x02 \x01(\t\x12\x0e\n\x06update\x18\x03 \x01(\t\"\x90\x03\n\x11\x43omputeAutoscaler\x12\x1a\n\x12\x63reation_timestamp\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\n\n\x02id\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x0f\n\x07project\x18\x05 \x01(\t\x12\x11\n\tself_link\x18\x06 \x01(\t\x12\x0e\n\x06target\x18\x07 \x01(\t\x12\x0c\n\x04zone\x18\x08 \x01(\t\x12\x63\n\x12\x61utoscaling_policy\x18\t \x01(\x0b\x32G.oak9.tython.gcp.compute_autoscaler.ComputeAutoscalerXAutoscalingPolicy\x12P\n\x08timeouts\x18\n \x01(\x0b\x32>.oak9.tython.gcp.compute_autoscaler.ComputeAutoscalerXTimeouts\x12\x37\n\rresource_info\x18\x0b \x01(\x0b\x32 .oak9.tython.shared.ResourceInfob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gcp.gcp_compute_autoscaler_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _COMPUTEAUTOSCALERXAUTOSCALINGPOLICYXCPUUTILIZATION._serialized_start=93
  _COMPUTEAUTOSCALERXAUTOSCALINGPOLICYXCPUUTILIZATION._serialized_end=188
  _COMPUTEAUTOSCALERXAUTOSCALINGPOLICYXLOADBALANCINGUTILIZATION._serialized_start=190
  _COMPUTEAUTOSCALERXAUTOSCALINGPOLICYXLOADBALANCINGUTILIZATION._serialized_end=268
  _COMPUTEAUTOSCALERXAUTOSCALINGPOLICYXMETRIC._serialized_start=270
  _COMPUTEAUTOSCALERXAUTOSCALINGPOLICYXMETRIC._serialized_end=358
  _COMPUTEAUTOSCALERXAUTOSCALINGPOLICYXSCALEINCONTROLXMAXSCALEDINREPLICAS._serialized_start=360
  _COMPUTEAUTOSCALERXAUTOSCALINGPOLICYXSCALEINCONTROLXMAXSCALEDINREPLICAS._serialized_end=464
  _COMPUTEAUTOSCALERXAUTOSCALINGPOLICYXSCALEINCONTROL._serialized_start=467
  _COMPUTEAUTOSCALERXAUTOSCALINGPOLICYXSCALEINCONTROL._serialized_end=685
  _COMPUTEAUTOSCALERXAUTOSCALINGPOLICYXSCALINGSCHEDULES._serialized_start=688
  _COMPUTEAUTOSCALERXAUTOSCALINGPOLICYXSCALINGSCHEDULES._serialized_end=885
  _COMPUTEAUTOSCALERXAUTOSCALINGPOLICY._serialized_start=888
  _COMPUTEAUTOSCALERXAUTOSCALINGPOLICY._serialized_end=1583
  _COMPUTEAUTOSCALERXTIMEOUTS._serialized_start=1585
  _COMPUTEAUTOSCALERXTIMEOUTS._serialized_end=1661
  _COMPUTEAUTOSCALER._serialized_start=1664
  _COMPUTEAUTOSCALER._serialized_end=2064
# @@protoc_insertion_point(module_scope)
