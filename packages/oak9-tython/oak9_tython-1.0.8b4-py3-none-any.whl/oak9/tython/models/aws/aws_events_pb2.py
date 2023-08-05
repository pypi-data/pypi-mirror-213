# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: aws/aws_events.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14\x61ws/aws_events.proto\x12\x16oak9.tython.aws.events\x1a\x13shared/shared.proto\"l\n\x08\x45ventBus\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x19\n\x11\x65vent_source_name\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\"\xab\x01\n\x06\x45vents\x12\x33\n\tevent_bus\x18\x01 \x03(\x0b\x32 .oak9.tython.aws.events.EventBus\x12@\n\x10\x65vent_bus_policy\x18\x02 \x03(\x0b\x32&.oak9.tython.aws.events.EventBusPolicy\x12*\n\x04rule\x18\x03 \x03(\x0b\x32\x1c.oak9.tython.aws.events.Rule\"n\n\x17\x45ventBusPolicyCondition\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\r\n\x05value\x18\x02 \x01(\t\x12\x0b\n\x03key\x18\x03 \x01(\t\"\xde\x01\n\x0e\x45ventBusPolicy\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x16\n\x0e\x65vent_bus_name\x18\x02 \x01(\t\x12\x42\n\tcondition\x18\x03 \x01(\x0b\x32/.oak9.tython.aws.events.EventBusPolicyCondition\x12\x0e\n\x06\x61\x63tion\x18\x04 \x01(\t\x12\x14\n\x0cstatement_id\x18\x05 \x01(\t\x12\x11\n\tprincipal\x18\x06 \x01(\t\"a\n\x18RuleBatchArrayProperties\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0c\n\x04size\x18\x02 \x01(\x05\"c\n\x16RuleBatchRetryStrategy\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x10\n\x08\x61ttempts\x18\x02 \x01(\x05\"\x8c\x02\n\x13RuleBatchParameters\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12J\n\x10\x61rray_properties\x18\x02 \x01(\x0b\x32\x30.oak9.tython.aws.events.RuleBatchArrayProperties\x12\x16\n\x0ejob_definition\x18\x03 \x01(\t\x12\x10\n\x08job_name\x18\x04 \x01(\t\x12\x46\n\x0eretry_strategy\x18\x05 \x01(\x0b\x32..oak9.tython.aws.events.RuleBatchRetryStrategy\"\x96\x01\n\x17RuleAwsVpcConfiguration\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x18\n\x10\x61ssign_public_ip\x18\x02 \x01(\t\x12\x17\n\x0fsecurity_groups\x18\x03 \x03(\t\x12\x0f\n\x07subnets\x18\x04 \x03(\t\"\xa3\x01\n\x18RuleNetworkConfiguration\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12N\n\x15\x61ws_vpc_configuration\x18\x02 \x01(\x0b\x32/.oak9.tython.aws.events.RuleAwsVpcConfiguration\"\x8c\x02\n\x11RuleEcsParameters\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\r\n\x05group\x18\x02 \x01(\t\x12\x13\n\x0blaunch_type\x18\x03 \x01(\t\x12O\n\x15network_configuration\x18\x04 \x01(\x0b\x32\x30.oak9.tython.aws.events.RuleNetworkConfiguration\x12\x18\n\x10platform_version\x18\x05 \x01(\t\x12\x12\n\ntask_count\x18\x06 \x01(\x05\x12\x1b\n\x13task_definition_arn\x18\x07 \x01(\t\"\xa8\x03\n\x12RuleHttpParameters\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12[\n\x11header_parameters\x18\x02 \x03(\x0b\x32@.oak9.tython.aws.events.RuleHttpParameters.HeaderParametersEntry\x12\x1d\n\x15path_parameter_values\x18\x03 \x03(\t\x12\x66\n\x17query_string_parameters\x18\x04 \x03(\x0b\x32\x45.oak9.tython.aws.events.RuleHttpParameters.QueryStringParametersEntry\x1a\x37\n\x15HeaderParametersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a<\n\x1aQueryStringParametersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xf7\x01\n\x14RuleInputTransformer\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12X\n\x0finput_paths_map\x18\x02 \x03(\x0b\x32?.oak9.tython.aws.events.RuleInputTransformer.InputPathsMapEntry\x12\x16\n\x0einput_template\x18\x03 \x01(\t\x1a\x34\n\x12InputPathsMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"l\n\x15RuleKinesisParameters\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1a\n\x12partition_key_path\x18\x02 \x01(\t\"l\n\x14RuleRunCommandTarget\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0b\n\x03key\x18\x02 \x01(\t\x12\x0e\n\x06values\x18\x03 \x03(\t\"\x9e\x01\n\x18RuleRunCommandParameters\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12I\n\x13run_command_targets\x18\x02 \x03(\x0b\x32,.oak9.tython.aws.events.RuleRunCommandTarget\"f\n\x11RuleSqsParameters\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x18\n\x10message_group_id\x18\x02 \x01(\t\"\x8b\x05\n\nRuleTarget\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0b\n\x03\x61rn\x18\x02 \x01(\t\x12\x45\n\x10\x62\x61tch_parameters\x18\x03 \x01(\x0b\x32+.oak9.tython.aws.events.RuleBatchParameters\x12\x41\n\x0e\x65\x63s_parameters\x18\x04 \x01(\x0b\x32).oak9.tython.aws.events.RuleEcsParameters\x12\x43\n\x0fhttp_parameters\x18\x05 \x01(\x0b\x32*.oak9.tython.aws.events.RuleHttpParameters\x12\n\n\x02id\x18\x06 \x01(\t\x12\r\n\x05input\x18\x07 \x01(\t\x12\x12\n\ninput_path\x18\x08 \x01(\t\x12G\n\x11input_transformer\x18\t \x01(\x0b\x32,.oak9.tython.aws.events.RuleInputTransformer\x12I\n\x12kinesis_parameters\x18\n \x01(\x0b\x32-.oak9.tython.aws.events.RuleKinesisParameters\x12\x10\n\x08role_arn\x18\x0b \x01(\t\x12P\n\x16run_command_parameters\x18\x0c \x01(\x0b\x32\x30.oak9.tython.aws.events.RuleRunCommandParameters\x12\x41\n\x0esqs_parameters\x18\r \x01(\x0b\x32).oak9.tython.aws.events.RuleSqsParameters\"\xe9\x02\n\x04Rule\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x16\n\x0e\x65vent_bus_name\x18\x03 \x01(\t\x12\x45\n\revent_pattern\x18\x04 \x03(\x0b\x32..oak9.tython.aws.events.Rule.EventPatternEntry\x12\x0c\n\x04name\x18\x05 \x01(\t\x12\x10\n\x08role_arn\x18\x06 \x01(\t\x12\x1b\n\x13schedule_expression\x18\x07 \x01(\t\x12\r\n\x05state\x18\x08 \x01(\t\x12\x33\n\x07targets\x18\t \x03(\x0b\x32\".oak9.tython.aws.events.RuleTarget\x1a\x33\n\x11\x45ventPatternEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'aws.aws_events_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _RULEHTTPPARAMETERS_HEADERPARAMETERSENTRY._options = None
  _RULEHTTPPARAMETERS_HEADERPARAMETERSENTRY._serialized_options = b'8\001'
  _RULEHTTPPARAMETERS_QUERYSTRINGPARAMETERSENTRY._options = None
  _RULEHTTPPARAMETERS_QUERYSTRINGPARAMETERSENTRY._serialized_options = b'8\001'
  _RULEINPUTTRANSFORMER_INPUTPATHSMAPENTRY._options = None
  _RULEINPUTTRANSFORMER_INPUTPATHSMAPENTRY._serialized_options = b'8\001'
  _RULE_EVENTPATTERNENTRY._options = None
  _RULE_EVENTPATTERNENTRY._serialized_options = b'8\001'
  _EVENTBUS._serialized_start=69
  _EVENTBUS._serialized_end=177
  _EVENTS._serialized_start=180
  _EVENTS._serialized_end=351
  _EVENTBUSPOLICYCONDITION._serialized_start=353
  _EVENTBUSPOLICYCONDITION._serialized_end=463
  _EVENTBUSPOLICY._serialized_start=466
  _EVENTBUSPOLICY._serialized_end=688
  _RULEBATCHARRAYPROPERTIES._serialized_start=690
  _RULEBATCHARRAYPROPERTIES._serialized_end=787
  _RULEBATCHRETRYSTRATEGY._serialized_start=789
  _RULEBATCHRETRYSTRATEGY._serialized_end=888
  _RULEBATCHPARAMETERS._serialized_start=891
  _RULEBATCHPARAMETERS._serialized_end=1159
  _RULEAWSVPCCONFIGURATION._serialized_start=1162
  _RULEAWSVPCCONFIGURATION._serialized_end=1312
  _RULENETWORKCONFIGURATION._serialized_start=1315
  _RULENETWORKCONFIGURATION._serialized_end=1478
  _RULEECSPARAMETERS._serialized_start=1481
  _RULEECSPARAMETERS._serialized_end=1749
  _RULEHTTPPARAMETERS._serialized_start=1752
  _RULEHTTPPARAMETERS._serialized_end=2176
  _RULEHTTPPARAMETERS_HEADERPARAMETERSENTRY._serialized_start=2059
  _RULEHTTPPARAMETERS_HEADERPARAMETERSENTRY._serialized_end=2114
  _RULEHTTPPARAMETERS_QUERYSTRINGPARAMETERSENTRY._serialized_start=2116
  _RULEHTTPPARAMETERS_QUERYSTRINGPARAMETERSENTRY._serialized_end=2176
  _RULEINPUTTRANSFORMER._serialized_start=2179
  _RULEINPUTTRANSFORMER._serialized_end=2426
  _RULEINPUTTRANSFORMER_INPUTPATHSMAPENTRY._serialized_start=2374
  _RULEINPUTTRANSFORMER_INPUTPATHSMAPENTRY._serialized_end=2426
  _RULEKINESISPARAMETERS._serialized_start=2428
  _RULEKINESISPARAMETERS._serialized_end=2536
  _RULERUNCOMMANDTARGET._serialized_start=2538
  _RULERUNCOMMANDTARGET._serialized_end=2646
  _RULERUNCOMMANDPARAMETERS._serialized_start=2649
  _RULERUNCOMMANDPARAMETERS._serialized_end=2807
  _RULESQSPARAMETERS._serialized_start=2809
  _RULESQSPARAMETERS._serialized_end=2911
  _RULETARGET._serialized_start=2914
  _RULETARGET._serialized_end=3565
  _RULE._serialized_start=3568
  _RULE._serialized_end=3929
  _RULE_EVENTPATTERNENTRY._serialized_start=3878
  _RULE_EVENTPATTERNENTRY._serialized_end=3929
# @@protoc_insertion_point(module_scope)
