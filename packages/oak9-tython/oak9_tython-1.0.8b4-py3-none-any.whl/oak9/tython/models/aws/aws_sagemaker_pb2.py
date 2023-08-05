# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: aws/aws_sagemaker.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17\x61ws/aws_sagemaker.proto\x12\x19oak9.tython.aws.sagemaker\x1a\x13shared/shared.proto\"\x8e\x01\n\x17\x43odeRepositoryGitConfig\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x12\n\nsecret_arn\x18\x02 \x01(\t\x12\x0e\n\x06\x62ranch\x18\x03 \x01(\t\x12\x16\n\x0erepository_url\x18\x04 \x01(\t\"\xaf\x01\n\x0e\x43odeRepository\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1c\n\x14\x63ode_repository_name\x18\x02 \x01(\t\x12\x46\n\ngit_config\x18\x03 \x01(\x0b\x32\x32.oak9.tython.aws.sagemaker.CodeRepositoryGitConfig\"\xae\x04\n\tSageMaker\x12\x42\n\x0f\x63ode_repository\x18\x01 \x03(\x0b\x32).oak9.tython.aws.sagemaker.CodeRepository\x12\x35\n\x08\x65ndpoint\x18\x02 \x03(\x0b\x32#.oak9.tython.aws.sagemaker.Endpoint\x12\x42\n\x0f\x65ndpoint_config\x18\x03 \x03(\x0b\x32).oak9.tython.aws.sagemaker.EndpointConfig\x12/\n\x05model\x18\x04 \x03(\x0b\x32 .oak9.tython.aws.sagemaker.Model\x12J\n\x13monitoring_schedule\x18\x05 \x03(\x0b\x32-.oak9.tython.aws.sagemaker.MonitoringSchedule\x12\x46\n\x11notebook_instance\x18\x06 \x03(\x0b\x32+.oak9.tython.aws.sagemaker.NotebookInstance\x12\x66\n\"notebook_instance_lifecycle_config\x18\x07 \x03(\x0b\x32:.oak9.tython.aws.sagemaker.NotebookInstanceLifecycleConfig\x12\x35\n\x08workteam\x18\x08 \x03(\x0b\x32#.oak9.tython.aws.sagemaker.Workteam\"q\n\x17\x45ndpointVariantProperty\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1d\n\x15variant_property_type\x18\x02 \x01(\t\"\xea\x02\n\x08\x45ndpoint\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12%\n\x1dretain_all_variant_properties\x18\x02 \x01(\x08\x12\x15\n\rendpoint_name\x18\x03 \x01(\t\x12_\n#exclude_retained_variant_properties\x18\x04 \x03(\x0b\x32\x32.oak9.tython.aws.sagemaker.EndpointVariantProperty\x12\x1c\n\x14\x65ndpoint_config_name\x18\x05 \x01(\t\x12;\n\x04tags\x18\x06 \x03(\x0b\x32-.oak9.tython.aws.sagemaker.Endpoint.TagsEntry\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"l\n\x1b\x45ndpointConfigCaptureOption\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x14\n\x0c\x63\x61pture_mode\x18\x02 \x01(\t\"\x98\x01\n&EndpointConfigCaptureContentTypeHeader\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1a\n\x12json_content_types\x18\x02 \x03(\t\x12\x19\n\x11\x63sv_content_types\x18\x03 \x03(\t\"\x80\x03\n\x1f\x45ndpointConfigDataCaptureConfig\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12O\n\x0f\x63\x61pture_options\x18\x02 \x03(\x0b\x32\x36.oak9.tython.aws.sagemaker.EndpointConfigCaptureOption\x12\x12\n\nkms_key_id\x18\x03 \x01(\t\x12\x1a\n\x12\x64\x65stination_s3_uri\x18\x04 \x01(\t\x12#\n\x1binitial_sampling_percentage\x18\x05 \x01(\x05\x12\x66\n\x1b\x63\x61pture_content_type_header\x18\x06 \x01(\x0b\x32\x41.oak9.tython.aws.sagemaker.EndpointConfigCaptureContentTypeHeader\x12\x16\n\x0e\x65nable_capture\x18\x07 \x01(\x08\"\xf5\x01\n\x1f\x45ndpointConfigProductionVariant\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x12\n\nmodel_name\x18\x02 \x01(\t\x12\x14\n\x0cvariant_name\x18\x03 \x01(\t\x12\x1e\n\x16initial_instance_count\x18\x04 \x01(\x05\x12\x15\n\rinstance_type\x18\x05 \x01(\t\x12\x18\n\x10\x61\x63\x63\x65lerator_type\x18\x06 \x01(\t\x12\x1e\n\x16initial_variant_weight\x18\x07 \x01(\x01\"\x9d\x03\n\x0e\x45ndpointConfig\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12W\n\x13\x64\x61ta_capture_config\x18\x02 \x01(\x0b\x32:.oak9.tython.aws.sagemaker.EndpointConfigDataCaptureConfig\x12W\n\x13production_variants\x18\x03 \x03(\x0b\x32:.oak9.tython.aws.sagemaker.EndpointConfigProductionVariant\x12\x12\n\nkms_key_id\x18\x04 \x01(\t\x12\x1c\n\x14\x65ndpoint_config_name\x18\x05 \x01(\t\x12\x41\n\x04tags\x18\x06 \x03(\x0b\x32\x33.oak9.tython.aws.sagemaker.EndpointConfig.TagsEntry\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xcf\x02\n\x18ModelContainerDefinition\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1a\n\x12\x63ontainer_hostname\x18\x02 \x01(\t\x12\x1a\n\x12model_package_name\x18\x03 \x01(\t\x12\x0c\n\x04mode\x18\x04 \x01(\t\x12Y\n\x0b\x65nvironment\x18\x05 \x03(\x0b\x32\x44.oak9.tython.aws.sagemaker.ModelContainerDefinition.EnvironmentEntry\x12\x16\n\x0emodel_data_url\x18\x06 \x01(\t\x12\r\n\x05image\x18\x07 \x01(\t\x1a\x32\n\x10\x45nvironmentEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"v\n\x0eModelVpcConfig\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0f\n\x07subnets\x18\x02 \x03(\t\x12\x1a\n\x12security_group_ids\x18\x03 \x03(\t\"\xd1\x03\n\x05Model\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1a\n\x12\x65xecution_role_arn\x18\x02 \x01(\t\x12 \n\x18\x65nable_network_isolation\x18\x03 \x01(\x08\x12N\n\x11primary_container\x18\x04 \x01(\x0b\x32\x33.oak9.tython.aws.sagemaker.ModelContainerDefinition\x12\x12\n\nmodel_name\x18\x05 \x01(\t\x12=\n\nvpc_config\x18\x06 \x01(\x0b\x32).oak9.tython.aws.sagemaker.ModelVpcConfig\x12G\n\ncontainers\x18\x07 \x03(\x0b\x32\x33.oak9.tython.aws.sagemaker.ModelContainerDefinition\x12\x38\n\x04tags\x18\x08 \x03(\x0b\x32*.oak9.tython.aws.sagemaker.Model.TagsEntry\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"p\n%MonitoringScheduleConstraintsResource\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0e\n\x06s3_uri\x18\x02 \x01(\t\"o\n$MonitoringScheduleStatisticsResource\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0e\n\x06s3_uri\x18\x02 \x01(\t\"\x99\x02\n MonitoringScheduleBaselineConfig\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12^\n\x14\x63onstraints_resource\x18\x02 \x01(\x0b\x32@.oak9.tython.aws.sagemaker.MonitoringScheduleConstraintsResource\x12\\\n\x13statistics_resource\x18\x03 \x01(\x0b\x32?.oak9.tython.aws.sagemaker.MonitoringScheduleStatisticsResource\"X\n\x1dMonitoringScheduleEnvironment\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\"\x8a\x02\n,MonitoringScheduleMonitoringAppSpecification\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1b\n\x13\x63ontainer_arguments\x18\x02 \x03(\t\x12\x1c\n\x14\x63ontainer_entrypoint\x18\x03 \x03(\t\x12\x11\n\timage_uri\x18\x04 \x01(\t\x12+\n#post_analytics_processor_source_uri\x18\x05 \x01(\t\x12&\n\x1erecord_preprocessor_source_uri\x18\x06 \x01(\t\"\xbf\x01\n\x1fMonitoringScheduleEndpointInput\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x15\n\rendpoint_name\x18\x02 \x01(\t\x12\x12\n\nlocal_path\x18\x03 \x01(\t\x12!\n\x19s3_data_distribution_type\x18\x04 \x01(\t\x12\x15\n\rs3_input_mode\x18\x05 \x01(\t\"\xb0\x01\n!MonitoringScheduleMonitoringInput\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12R\n\x0e\x65ndpoint_input\x18\x02 \x01(\x0b\x32:.oak9.tython.aws.sagemaker.MonitoringScheduleEndpointInput\"\xb6\x01\n\"MonitoringScheduleMonitoringInputs\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12W\n\x11monitoring_inputs\x18\x02 \x03(\x0b\x32<.oak9.tython.aws.sagemaker.MonitoringScheduleMonitoringInput\"\x91\x01\n\x1aMonitoringScheduleS3Output\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x12\n\nlocal_path\x18\x02 \x01(\t\x12\x16\n\x0es3_upload_mode\x18\x03 \x01(\t\x12\x0e\n\x06s3_uri\x18\x04 \x01(\t\"\xa7\x01\n\"MonitoringScheduleMonitoringOutput\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12H\n\ts3_output\x18\x02 \x01(\x0b\x32\x35.oak9.tython.aws.sagemaker.MonitoringScheduleS3Output\"\xd2\x01\n(MonitoringScheduleMonitoringOutputConfig\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x12\n\nkms_key_id\x18\x02 \x01(\t\x12Y\n\x12monitoring_outputs\x18\x03 \x03(\x0b\x32=.oak9.tython.aws.sagemaker.MonitoringScheduleMonitoringOutput\"\xbf\x01\n\x1fMonitoringScheduleClusterConfig\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x16\n\x0einstance_count\x18\x02 \x01(\x05\x12\x15\n\rinstance_type\x18\x03 \x01(\t\x12\x19\n\x11volume_kms_key_id\x18\x04 \x01(\t\x12\x19\n\x11volume_size_in_gb\x18\x05 \x01(\x05\"\xb4\x01\n%MonitoringScheduleMonitoringResources\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12R\n\x0e\x63luster_config\x18\x02 \x01(\x0b\x32:.oak9.tython.aws.sagemaker.MonitoringScheduleClusterConfig\"\x83\x01\n\x1bMonitoringScheduleVpcConfig\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1a\n\x12security_group_ids\x18\x02 \x03(\t\x12\x0f\n\x07subnets\x18\x03 \x03(\t\"\xfb\x01\n\x1fMonitoringScheduleNetworkConfig\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x31\n)enable_inter_container_traffic_encryption\x18\x02 \x01(\x08\x12 \n\x18\x65nable_network_isolation\x18\x03 \x01(\x08\x12J\n\nvpc_config\x18\x04 \x01(\x0b\x32\x36.oak9.tython.aws.sagemaker.MonitoringScheduleVpcConfig\"~\n#MonitoringScheduleStoppingCondition\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1e\n\x16max_runtime_in_seconds\x18\x02 \x01(\x05\"\xdb\x06\n)MonitoringScheduleMonitoringJobDefinition\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12T\n\x0f\x62\x61seline_config\x18\x02 \x01(\x0b\x32;.oak9.tython.aws.sagemaker.MonitoringScheduleBaselineConfig\x12M\n\x0b\x65nvironment\x18\x03 \x01(\x0b\x32\x38.oak9.tython.aws.sagemaker.MonitoringScheduleEnvironment\x12m\n\x1cmonitoring_app_specification\x18\x04 \x01(\x0b\x32G.oak9.tython.aws.sagemaker.MonitoringScheduleMonitoringAppSpecification\x12X\n\x11monitoring_inputs\x18\x05 \x01(\x0b\x32=.oak9.tython.aws.sagemaker.MonitoringScheduleMonitoringInputs\x12\x65\n\x18monitoring_output_config\x18\x06 \x01(\x0b\x32\x43.oak9.tython.aws.sagemaker.MonitoringScheduleMonitoringOutputConfig\x12^\n\x14monitoring_resources\x18\x07 \x01(\x0b\x32@.oak9.tython.aws.sagemaker.MonitoringScheduleMonitoringResources\x12R\n\x0enetwork_config\x18\x08 \x01(\x0b\x32:.oak9.tython.aws.sagemaker.MonitoringScheduleNetworkConfig\x12\x10\n\x08role_arn\x18\t \x01(\t\x12Z\n\x12stopping_condition\x18\n \x01(\x0b\x32>.oak9.tython.aws.sagemaker.MonitoringScheduleStoppingCondition\"x\n MonitoringScheduleScheduleConfig\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1b\n\x13schedule_expression\x18\x02 \x01(\t\"\xa4\x02\n*MonitoringScheduleMonitoringScheduleConfig\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12g\n\x19monitoring_job_definition\x18\x02 \x01(\x0b\x32\x44.oak9.tython.aws.sagemaker.MonitoringScheduleMonitoringJobDefinition\x12T\n\x0fschedule_config\x18\x03 \x01(\x0b\x32;.oak9.tython.aws.sagemaker.MonitoringScheduleScheduleConfig\"\xc4\x02\n,MonitoringScheduleMonitoringExecutionSummary\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x15\n\rcreation_time\x18\x02 \x01(\t\x12\x15\n\rendpoint_name\x18\x03 \x01(\t\x12\x16\n\x0e\x66\x61ilure_reason\x18\x04 \x01(\t\x12\x1a\n\x12last_modified_time\x18\x05 \x01(\t\x12#\n\x1bmonitoring_execution_status\x18\x06 \x01(\t\x12 \n\x18monitoring_schedule_name\x18\x07 \x01(\t\x12\x1a\n\x12processing_job_arn\x18\x08 \x01(\t\x12\x16\n\x0escheduled_time\x18\t \x01(\t\"\xe9\x04\n\x12MonitoringSchedule\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1f\n\x17monitoring_schedule_arn\x18\x02 \x01(\t\x12 \n\x18monitoring_schedule_name\x18\x03 \x01(\t\x12i\n\x1amonitoring_schedule_config\x18\x04 \x01(\x0b\x32\x45.oak9.tython.aws.sagemaker.MonitoringScheduleMonitoringScheduleConfig\x12\x45\n\x04tags\x18\x05 \x03(\x0b\x32\x37.oak9.tython.aws.sagemaker.MonitoringSchedule.TagsEntry\x12\x15\n\rcreation_time\x18\x06 \x01(\t\x12\x15\n\rendpoint_name\x18\x07 \x01(\t\x12\x16\n\x0e\x66\x61ilure_reason\x18\x08 \x01(\t\x12\x1a\n\x12last_modified_time\x18\t \x01(\t\x12r\n!last_monitoring_execution_summary\x18\n \x01(\x0b\x32G.oak9.tython.aws.sagemaker.MonitoringScheduleMonitoringExecutionSummary\x12\"\n\x1amonitoring_schedule_status\x18\x0b \x01(\t\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x9a\x04\n\x10NotebookInstance\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x12\n\nkms_key_id\x18\x02 \x01(\t\x12\x19\n\x11volume_size_in_gb\x18\x03 \x01(\x05\x12$\n\x1c\x61\x64\x64itional_code_repositories\x18\x04 \x03(\t\x12\x1f\n\x17\x64\x65\x66\x61ult_code_repository\x18\x05 \x01(\t\x12\x1e\n\x16\x64irect_internet_access\x18\x06 \x01(\t\x12\x19\n\x11\x61\x63\x63\x65lerator_types\x18\x07 \x03(\t\x12\x11\n\tsubnet_id\x18\x08 \x01(\t\x12\x1a\n\x12security_group_ids\x18\t \x03(\t\x12\x10\n\x08role_arn\x18\n \x01(\t\x12\x13\n\x0broot_access\x18\x0b \x01(\t\x12\x1e\n\x16notebook_instance_name\x18\x0c \x01(\t\x12\x15\n\rinstance_type\x18\r \x01(\t\x12\x1d\n\x15lifecycle_config_name\x18\x0e \x01(\t\x12\x43\n\x04tags\x18\x0f \x03(\x0b\x32\x35.oak9.tython.aws.sagemaker.NotebookInstance.TagsEntry\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x88\x01\n<NotebookInstanceLifecycleConfigNotebookInstanceLifecycleHook\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\"\xe2\x02\n\x1fNotebookInstanceLifecycleConfig\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12i\n\x08on_start\x18\x02 \x03(\x0b\x32W.oak9.tython.aws.sagemaker.NotebookInstanceLifecycleConfigNotebookInstanceLifecycleHook\x12/\n\'notebook_instance_lifecycle_config_name\x18\x03 \x01(\t\x12j\n\ton_create\x18\x04 \x03(\x0b\x32W.oak9.tython.aws.sagemaker.NotebookInstanceLifecycleConfigNotebookInstanceLifecycleHook\"|\n!WorkteamNotificationConfiguration\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x1e\n\x16notification_topic_arn\x18\x02 \x01(\t\"\xac\x01\n\x1fWorkteamCognitoMemberDefinition\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x19\n\x11\x63ognito_user_pool\x18\x02 \x01(\t\x12\x19\n\x11\x63ognito_client_id\x18\x03 \x01(\t\x12\x1a\n\x12\x63ognito_user_group\x18\x04 \x01(\t\"\xb2\x01\n\x18WorkteamMemberDefinition\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12]\n\x19\x63ognito_member_definition\x18\x02 \x01(\x0b\x32:.oak9.tython.aws.sagemaker.WorkteamCognitoMemberDefinition\"\x8c\x03\n\x08Workteam\x12\x37\n\rresource_info\x18\x01 \x01(\x0b\x32 .oak9.tython.shared.ResourceInfo\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12`\n\x1anotification_configuration\x18\x03 \x01(\x0b\x32<.oak9.tython.aws.sagemaker.WorkteamNotificationConfiguration\x12\x15\n\rworkteam_name\x18\x04 \x01(\t\x12O\n\x12member_definitions\x18\x05 \x03(\x0b\x32\x33.oak9.tython.aws.sagemaker.WorkteamMemberDefinition\x12;\n\x04tags\x18\x06 \x03(\x0b\x32-.oak9.tython.aws.sagemaker.Workteam.TagsEntry\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'aws.aws_sagemaker_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ENDPOINT_TAGSENTRY._options = None
  _ENDPOINT_TAGSENTRY._serialized_options = b'8\001'
  _ENDPOINTCONFIG_TAGSENTRY._options = None
  _ENDPOINTCONFIG_TAGSENTRY._serialized_options = b'8\001'
  _MODELCONTAINERDEFINITION_ENVIRONMENTENTRY._options = None
  _MODELCONTAINERDEFINITION_ENVIRONMENTENTRY._serialized_options = b'8\001'
  _MODEL_TAGSENTRY._options = None
  _MODEL_TAGSENTRY._serialized_options = b'8\001'
  _MONITORINGSCHEDULE_TAGSENTRY._options = None
  _MONITORINGSCHEDULE_TAGSENTRY._serialized_options = b'8\001'
  _NOTEBOOKINSTANCE_TAGSENTRY._options = None
  _NOTEBOOKINSTANCE_TAGSENTRY._serialized_options = b'8\001'
  _WORKTEAM_TAGSENTRY._options = None
  _WORKTEAM_TAGSENTRY._serialized_options = b'8\001'
  _CODEREPOSITORYGITCONFIG._serialized_start=76
  _CODEREPOSITORYGITCONFIG._serialized_end=218
  _CODEREPOSITORY._serialized_start=221
  _CODEREPOSITORY._serialized_end=396
  _SAGEMAKER._serialized_start=399
  _SAGEMAKER._serialized_end=957
  _ENDPOINTVARIANTPROPERTY._serialized_start=959
  _ENDPOINTVARIANTPROPERTY._serialized_end=1072
  _ENDPOINT._serialized_start=1075
  _ENDPOINT._serialized_end=1437
  _ENDPOINT_TAGSENTRY._serialized_start=1394
  _ENDPOINT_TAGSENTRY._serialized_end=1437
  _ENDPOINTCONFIGCAPTUREOPTION._serialized_start=1439
  _ENDPOINTCONFIGCAPTUREOPTION._serialized_end=1547
  _ENDPOINTCONFIGCAPTURECONTENTTYPEHEADER._serialized_start=1550
  _ENDPOINTCONFIGCAPTURECONTENTTYPEHEADER._serialized_end=1702
  _ENDPOINTCONFIGDATACAPTURECONFIG._serialized_start=1705
  _ENDPOINTCONFIGDATACAPTURECONFIG._serialized_end=2089
  _ENDPOINTCONFIGPRODUCTIONVARIANT._serialized_start=2092
  _ENDPOINTCONFIGPRODUCTIONVARIANT._serialized_end=2337
  _ENDPOINTCONFIG._serialized_start=2340
  _ENDPOINTCONFIG._serialized_end=2753
  _ENDPOINTCONFIG_TAGSENTRY._serialized_start=1394
  _ENDPOINTCONFIG_TAGSENTRY._serialized_end=1437
  _MODELCONTAINERDEFINITION._serialized_start=2756
  _MODELCONTAINERDEFINITION._serialized_end=3091
  _MODELCONTAINERDEFINITION_ENVIRONMENTENTRY._serialized_start=3041
  _MODELCONTAINERDEFINITION_ENVIRONMENTENTRY._serialized_end=3091
  _MODELVPCCONFIG._serialized_start=3093
  _MODELVPCCONFIG._serialized_end=3211
  _MODEL._serialized_start=3214
  _MODEL._serialized_end=3679
  _MODEL_TAGSENTRY._serialized_start=1394
  _MODEL_TAGSENTRY._serialized_end=1437
  _MONITORINGSCHEDULECONSTRAINTSRESOURCE._serialized_start=3681
  _MONITORINGSCHEDULECONSTRAINTSRESOURCE._serialized_end=3793
  _MONITORINGSCHEDULESTATISTICSRESOURCE._serialized_start=3795
  _MONITORINGSCHEDULESTATISTICSRESOURCE._serialized_end=3906
  _MONITORINGSCHEDULEBASELINECONFIG._serialized_start=3909
  _MONITORINGSCHEDULEBASELINECONFIG._serialized_end=4190
  _MONITORINGSCHEDULEENVIRONMENT._serialized_start=4192
  _MONITORINGSCHEDULEENVIRONMENT._serialized_end=4280
  _MONITORINGSCHEDULEMONITORINGAPPSPECIFICATION._serialized_start=4283
  _MONITORINGSCHEDULEMONITORINGAPPSPECIFICATION._serialized_end=4549
  _MONITORINGSCHEDULEENDPOINTINPUT._serialized_start=4552
  _MONITORINGSCHEDULEENDPOINTINPUT._serialized_end=4743
  _MONITORINGSCHEDULEMONITORINGINPUT._serialized_start=4746
  _MONITORINGSCHEDULEMONITORINGINPUT._serialized_end=4922
  _MONITORINGSCHEDULEMONITORINGINPUTS._serialized_start=4925
  _MONITORINGSCHEDULEMONITORINGINPUTS._serialized_end=5107
  _MONITORINGSCHEDULES3OUTPUT._serialized_start=5110
  _MONITORINGSCHEDULES3OUTPUT._serialized_end=5255
  _MONITORINGSCHEDULEMONITORINGOUTPUT._serialized_start=5258
  _MONITORINGSCHEDULEMONITORINGOUTPUT._serialized_end=5425
  _MONITORINGSCHEDULEMONITORINGOUTPUTCONFIG._serialized_start=5428
  _MONITORINGSCHEDULEMONITORINGOUTPUTCONFIG._serialized_end=5638
  _MONITORINGSCHEDULECLUSTERCONFIG._serialized_start=5641
  _MONITORINGSCHEDULECLUSTERCONFIG._serialized_end=5832
  _MONITORINGSCHEDULEMONITORINGRESOURCES._serialized_start=5835
  _MONITORINGSCHEDULEMONITORINGRESOURCES._serialized_end=6015
  _MONITORINGSCHEDULEVPCCONFIG._serialized_start=6018
  _MONITORINGSCHEDULEVPCCONFIG._serialized_end=6149
  _MONITORINGSCHEDULENETWORKCONFIG._serialized_start=6152
  _MONITORINGSCHEDULENETWORKCONFIG._serialized_end=6403
  _MONITORINGSCHEDULESTOPPINGCONDITION._serialized_start=6405
  _MONITORINGSCHEDULESTOPPINGCONDITION._serialized_end=6531
  _MONITORINGSCHEDULEMONITORINGJOBDEFINITION._serialized_start=6534
  _MONITORINGSCHEDULEMONITORINGJOBDEFINITION._serialized_end=7393
  _MONITORINGSCHEDULESCHEDULECONFIG._serialized_start=7395
  _MONITORINGSCHEDULESCHEDULECONFIG._serialized_end=7515
  _MONITORINGSCHEDULEMONITORINGSCHEDULECONFIG._serialized_start=7518
  _MONITORINGSCHEDULEMONITORINGSCHEDULECONFIG._serialized_end=7810
  _MONITORINGSCHEDULEMONITORINGEXECUTIONSUMMARY._serialized_start=7813
  _MONITORINGSCHEDULEMONITORINGEXECUTIONSUMMARY._serialized_end=8137
  _MONITORINGSCHEDULE._serialized_start=8140
  _MONITORINGSCHEDULE._serialized_end=8757
  _MONITORINGSCHEDULE_TAGSENTRY._serialized_start=1394
  _MONITORINGSCHEDULE_TAGSENTRY._serialized_end=1437
  _NOTEBOOKINSTANCE._serialized_start=8760
  _NOTEBOOKINSTANCE._serialized_end=9298
  _NOTEBOOKINSTANCE_TAGSENTRY._serialized_start=1394
  _NOTEBOOKINSTANCE_TAGSENTRY._serialized_end=1437
  _NOTEBOOKINSTANCELIFECYCLECONFIGNOTEBOOKINSTANCELIFECYCLEHOOK._serialized_start=9301
  _NOTEBOOKINSTANCELIFECYCLECONFIGNOTEBOOKINSTANCELIFECYCLEHOOK._serialized_end=9437
  _NOTEBOOKINSTANCELIFECYCLECONFIG._serialized_start=9440
  _NOTEBOOKINSTANCELIFECYCLECONFIG._serialized_end=9794
  _WORKTEAMNOTIFICATIONCONFIGURATION._serialized_start=9796
  _WORKTEAMNOTIFICATIONCONFIGURATION._serialized_end=9920
  _WORKTEAMCOGNITOMEMBERDEFINITION._serialized_start=9923
  _WORKTEAMCOGNITOMEMBERDEFINITION._serialized_end=10095
  _WORKTEAMMEMBERDEFINITION._serialized_start=10098
  _WORKTEAMMEMBERDEFINITION._serialized_end=10276
  _WORKTEAM._serialized_start=10279
  _WORKTEAM._serialized_end=10675
  _WORKTEAM_TAGSENTRY._serialized_start=1394
  _WORKTEAM_TAGSENTRY._serialized_end=1437
# @@protoc_insertion_point(module_scope)
