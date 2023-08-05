# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: aws/aws_autoscalingplans.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1e\x61ws/aws_autoscalingplans.proto\x12 oak9.tython.aws.autoscalingplans\x1a\x13shared/shared.proto\"l\n\x14ScalingPlanTagFilter\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0e\n\x06values\x18\x02 \x03(\t\x12\x0b\n\x03key\x18\x03 \x01(\t\"\xc7\x01\n\x1cScalingPlanApplicationSource\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12!\n\x19\x63loud_formation_stack_arn\x18\x02 \x01(\t\x12K\n\x0btag_filters\x18\x03 \x03(\x0b\x32\x36.oak9.tython.aws.autoscalingplans.ScalingPlanTagFilter\"\xaa\x01\n/ScalingPlanPredefinedScalingMetricSpecification\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x16\n\x0eresource_label\x18\x02 \x01(\t\x12&\n\x1epredefined_scaling_metric_type\x18\x03 \x01(\t\"r\n\x1aScalingPlanMetricDimension\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\r\n\x05value\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\"\x85\x02\n/ScalingPlanCustomizedScalingMetricSpecification\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x13\n\x0bmetric_name\x18\x02 \x01(\t\x12\x11\n\tstatistic\x18\x03 \x01(\t\x12P\n\ndimensions\x18\x04 \x03(\x0b\x32<.oak9.tython.aws.autoscalingplans.ScalingPlanMetricDimension\x12\x0c\n\x04unit\x18\x05 \x01(\t\x12\x11\n\tnamespace\x18\x06 \x01(\t\"\xf5\x03\n&ScalingPlanTargetTrackingConfiguration\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1a\n\x12scale_out_cooldown\x18\x02 \x01(\x05\x12\x14\n\x0ctarget_value\x18\x03 \x01(\x01\x12\x82\x01\n\'predefined_scaling_metric_specification\x18\x04 \x01(\x0b\x32Q.oak9.tython.aws.autoscalingplans.ScalingPlanPredefinedScalingMetricSpecification\x12\x18\n\x10\x64isable_scale_in\x18\x05 \x01(\x08\x12\x19\n\x11scale_in_cooldown\x18\x06 \x01(\x05\x12!\n\x19\x65stimated_instance_warmup\x18\x07 \x01(\x05\x12\x82\x01\n\'customized_scaling_metric_specification\x18\x08 \x01(\x0b\x32Q.oak9.tython.aws.autoscalingplans.ScalingPlanCustomizedScalingMetricSpecification\"\x82\x02\n,ScalingPlanCustomizedLoadMetricSpecification\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x13\n\x0bmetric_name\x18\x02 \x01(\t\x12\x11\n\tstatistic\x18\x03 \x01(\t\x12P\n\ndimensions\x18\x04 \x03(\x0b\x32<.oak9.tython.aws.autoscalingplans.ScalingPlanMetricDimension\x12\x0c\n\x04unit\x18\x05 \x01(\t\x12\x11\n\tnamespace\x18\x06 \x01(\t\"\xa4\x01\n,ScalingPlanPredefinedLoadMetricSpecification\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12#\n\x1bpredefined_load_metric_type\x18\x02 \x01(\t\x12\x16\n\x0eresource_label\x18\x03 \x01(\t\"\xb0\x06\n\x1dScalingPlanScalingInstruction\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1f\n\x17\x64isable_dynamic_scaling\x18\x02 \x01(\x08\x12\x19\n\x11service_namespace\x18\x03 \x01(\t\x12\x30\n(predictive_scaling_max_capacity_behavior\x18\x04 \x01(\t\x12\x1a\n\x12scalable_dimension\x18\x05 \x01(\t\x12&\n\x1escaling_policy_update_behavior\x18\x06 \x01(\t\x12\x14\n\x0cmin_capacity\x18\x07 \x01(\x05\x12p\n\x1etarget_tracking_configurations\x18\x08 \x03(\x0b\x32H.oak9.tython.aws.autoscalingplans.ScalingPlanTargetTrackingConfiguration\x12.\n&predictive_scaling_max_capacity_buffer\x18\t \x01(\x05\x12|\n$customized_load_metric_specification\x18\n \x01(\x0b\x32N.oak9.tython.aws.autoscalingplans.ScalingPlanCustomizedLoadMetricSpecification\x12|\n$predefined_load_metric_specification\x18\x0b \x01(\x0b\x32N.oak9.tython.aws.autoscalingplans.ScalingPlanPredefinedLoadMetricSpecification\x12\x13\n\x0bresource_id\x18\x0c \x01(\t\x12$\n\x1cscheduled_action_buffer_time\x18\r \x01(\x05\x12\x14\n\x0cmax_capacity\x18\x0e \x01(\x05\x12\x1f\n\x17predictive_scaling_mode\x18\x0f \x01(\t\"\x81\x02\n\x0bScalingPlan\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12Z\n\x12\x61pplication_source\x18\x02 \x01(\x0b\x32>.oak9.tython.aws.autoscalingplans.ScalingPlanApplicationSource\x12]\n\x14scaling_instructions\x18\x03 \x03(\x0b\x32?.oak9.tython.aws.autoscalingplans.ScalingPlanScalingInstruction\"W\n\x10\x41utoScalingPlans\x12\x43\n\x0cscaling_plan\x18\x01 \x03(\x0b\x32-.oak9.tython.aws.autoscalingplans.ScalingPlanb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'aws.aws_autoscalingplans_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SCALINGPLANTAGFILTER._serialized_start=89
  _SCALINGPLANTAGFILTER._serialized_end=197
  _SCALINGPLANAPPLICATIONSOURCE._serialized_start=200
  _SCALINGPLANAPPLICATIONSOURCE._serialized_end=399
  _SCALINGPLANPREDEFINEDSCALINGMETRICSPECIFICATION._serialized_start=402
  _SCALINGPLANPREDEFINEDSCALINGMETRICSPECIFICATION._serialized_end=572
  _SCALINGPLANMETRICDIMENSION._serialized_start=574
  _SCALINGPLANMETRICDIMENSION._serialized_end=688
  _SCALINGPLANCUSTOMIZEDSCALINGMETRICSPECIFICATION._serialized_start=691
  _SCALINGPLANCUSTOMIZEDSCALINGMETRICSPECIFICATION._serialized_end=952
  _SCALINGPLANTARGETTRACKINGCONFIGURATION._serialized_start=955
  _SCALINGPLANTARGETTRACKINGCONFIGURATION._serialized_end=1456
  _SCALINGPLANCUSTOMIZEDLOADMETRICSPECIFICATION._serialized_start=1459
  _SCALINGPLANCUSTOMIZEDLOADMETRICSPECIFICATION._serialized_end=1717
  _SCALINGPLANPREDEFINEDLOADMETRICSPECIFICATION._serialized_start=1720
  _SCALINGPLANPREDEFINEDLOADMETRICSPECIFICATION._serialized_end=1884
  _SCALINGPLANSCALINGINSTRUCTION._serialized_start=1887
  _SCALINGPLANSCALINGINSTRUCTION._serialized_end=2703
  _SCALINGPLAN._serialized_start=2706
  _SCALINGPLAN._serialized_end=2963
  _AUTOSCALINGPLANS._serialized_start=2965
  _AUTOSCALINGPLANS._serialized_end=3052
# @@protoc_insertion_point(module_scope)
