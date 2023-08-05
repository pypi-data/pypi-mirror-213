"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import shared.shared_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class CustomActionTypeConfigurationProperties(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    KEY_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    QUERYABLE_FIELD_NUMBER: builtins.int
    REQUIRED_FIELD_NUMBER: builtins.int
    SECRET_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    description: builtins.str
    key: builtins.bool
    name: builtins.str
    queryable: builtins.bool
    required: builtins.bool
    secret: builtins.bool
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        description: builtins.str = ...,
        key: builtins.bool = ...,
        name: builtins.str = ...,
        queryable: builtins.bool = ...,
        required: builtins.bool = ...,
        secret: builtins.bool = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["description", b"description", "key", b"key", "name", b"name", "queryable", b"queryable", "required", b"required", "resource_info", b"resource_info", "secret", b"secret"]) -> None: ...

global___CustomActionTypeConfigurationProperties = CustomActionTypeConfigurationProperties

@typing_extensions.final
class CustomActionTypeArtifactDetails(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    MAXIMUM_COUNT_FIELD_NUMBER: builtins.int
    MINIMUM_COUNT_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    maximum_count: builtins.int
    minimum_count: builtins.int
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        maximum_count: builtins.int = ...,
        minimum_count: builtins.int = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["maximum_count", b"maximum_count", "minimum_count", b"minimum_count", "resource_info", b"resource_info"]) -> None: ...

global___CustomActionTypeArtifactDetails = CustomActionTypeArtifactDetails

@typing_extensions.final
class CustomActionTypeSettings(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    ENTITY_URL_TEMPLATE_FIELD_NUMBER: builtins.int
    EXECUTION_URL_TEMPLATE_FIELD_NUMBER: builtins.int
    REVISION_URL_TEMPLATE_FIELD_NUMBER: builtins.int
    THIRD_PARTY_CONFIGURATION_URL_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    entity_url_template: builtins.str
    execution_url_template: builtins.str
    revision_url_template: builtins.str
    third_party_configuration_url: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        entity_url_template: builtins.str = ...,
        execution_url_template: builtins.str = ...,
        revision_url_template: builtins.str = ...,
        third_party_configuration_url: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["entity_url_template", b"entity_url_template", "execution_url_template", b"execution_url_template", "resource_info", b"resource_info", "revision_url_template", b"revision_url_template", "third_party_configuration_url", b"third_party_configuration_url"]) -> None: ...

global___CustomActionTypeSettings = CustomActionTypeSettings

@typing_extensions.final
class CustomActionType(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class TagsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.str
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    CATEGORY_FIELD_NUMBER: builtins.int
    CONFIGURATION_PROPERTIES_FIELD_NUMBER: builtins.int
    INPUT_ARTIFACT_DETAILS_FIELD_NUMBER: builtins.int
    OUTPUT_ARTIFACT_DETAILS_FIELD_NUMBER: builtins.int
    PROVIDER_FIELD_NUMBER: builtins.int
    SETTINGS_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    VERSION_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    category: builtins.str
    @property
    def configuration_properties(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___CustomActionTypeConfigurationProperties]: ...
    @property
    def input_artifact_details(self) -> global___CustomActionTypeArtifactDetails: ...
    @property
    def output_artifact_details(self) -> global___CustomActionTypeArtifactDetails: ...
    provider: builtins.str
    @property
    def settings(self) -> global___CustomActionTypeSettings: ...
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    version: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        category: builtins.str = ...,
        configuration_properties: collections.abc.Iterable[global___CustomActionTypeConfigurationProperties] | None = ...,
        input_artifact_details: global___CustomActionTypeArtifactDetails | None = ...,
        output_artifact_details: global___CustomActionTypeArtifactDetails | None = ...,
        provider: builtins.str = ...,
        settings: global___CustomActionTypeSettings | None = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        version: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["input_artifact_details", b"input_artifact_details", "output_artifact_details", b"output_artifact_details", "resource_info", b"resource_info", "settings", b"settings"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["category", b"category", "configuration_properties", b"configuration_properties", "input_artifact_details", b"input_artifact_details", "output_artifact_details", b"output_artifact_details", "provider", b"provider", "resource_info", b"resource_info", "settings", b"settings", "tags", b"tags", "version", b"version"]) -> None: ...

global___CustomActionType = CustomActionType

@typing_extensions.final
class CodePipeline(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CUSTOM_ACTION_TYPE_FIELD_NUMBER: builtins.int
    PIPELINE_FIELD_NUMBER: builtins.int
    WEBHOOK_FIELD_NUMBER: builtins.int
    @property
    def custom_action_type(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___CustomActionType]: ...
    @property
    def pipeline(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Pipeline]: ...
    @property
    def webhook(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Webhook]: ...
    def __init__(
        self,
        *,
        custom_action_type: collections.abc.Iterable[global___CustomActionType] | None = ...,
        pipeline: collections.abc.Iterable[global___Pipeline] | None = ...,
        webhook: collections.abc.Iterable[global___Webhook] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["custom_action_type", b"custom_action_type", "pipeline", b"pipeline", "webhook", b"webhook"]) -> None: ...

global___CodePipeline = CodePipeline

@typing_extensions.final
class PipelineEncryptionKey(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    id: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        id: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["id", b"id", "resource_info", b"resource_info"]) -> None: ...

global___PipelineEncryptionKey = PipelineEncryptionKey

@typing_extensions.final
class PipelineArtifactStore(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    ENCRYPTION_KEY_FIELD_NUMBER: builtins.int
    LOCATION_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def encryption_key(self) -> global___PipelineEncryptionKey: ...
    location: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        encryption_key: global___PipelineEncryptionKey | None = ...,
        location: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["encryption_key", b"encryption_key", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["encryption_key", b"encryption_key", "location", b"location", "resource_info", b"resource_info"]) -> None: ...

global___PipelineArtifactStore = PipelineArtifactStore

@typing_extensions.final
class PipelineArtifactStoreMap(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    ARTIFACT_STORE_FIELD_NUMBER: builtins.int
    REGION_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def artifact_store(self) -> global___PipelineArtifactStore: ...
    region: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        artifact_store: global___PipelineArtifactStore | None = ...,
        region: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["artifact_store", b"artifact_store", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["artifact_store", b"artifact_store", "region", b"region", "resource_info", b"resource_info"]) -> None: ...

global___PipelineArtifactStoreMap = PipelineArtifactStoreMap

@typing_extensions.final
class PipelineStageTransition(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    REASON_FIELD_NUMBER: builtins.int
    STAGE_NAME_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    reason: builtins.str
    stage_name: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        reason: builtins.str = ...,
        stage_name: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["reason", b"reason", "resource_info", b"resource_info", "stage_name", b"stage_name"]) -> None: ...

global___PipelineStageTransition = PipelineStageTransition

@typing_extensions.final
class PipelineActionTypeId(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    CATEGORY_FIELD_NUMBER: builtins.int
    OWNER_FIELD_NUMBER: builtins.int
    PROVIDER_FIELD_NUMBER: builtins.int
    VERSION_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    category: builtins.str
    owner: builtins.str
    provider: builtins.str
    version: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        category: builtins.str = ...,
        owner: builtins.str = ...,
        provider: builtins.str = ...,
        version: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["category", b"category", "owner", b"owner", "provider", b"provider", "resource_info", b"resource_info", "version", b"version"]) -> None: ...

global___PipelineActionTypeId = PipelineActionTypeId

@typing_extensions.final
class PipelineInputArtifact(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    name: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        name: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "resource_info", b"resource_info"]) -> None: ...

global___PipelineInputArtifact = PipelineInputArtifact

@typing_extensions.final
class PipelineOutputArtifact(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    name: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        name: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "resource_info", b"resource_info"]) -> None: ...

global___PipelineOutputArtifact = PipelineOutputArtifact

@typing_extensions.final
class PipelineActionDeclaration(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class ConfigurationEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.str
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    ACTION_TYPE_ID_FIELD_NUMBER: builtins.int
    CONFIGURATION_FIELD_NUMBER: builtins.int
    INPUT_ARTIFACTS_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    NAMESPACE_FIELD_NUMBER: builtins.int
    OUTPUT_ARTIFACTS_FIELD_NUMBER: builtins.int
    REGION_FIELD_NUMBER: builtins.int
    ROLE_ARN_FIELD_NUMBER: builtins.int
    RUN_ORDER_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def action_type_id(self) -> global___PipelineActionTypeId: ...
    @property
    def configuration(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    @property
    def input_artifacts(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___PipelineInputArtifact]: ...
    name: builtins.str
    namespace: builtins.str
    @property
    def output_artifacts(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___PipelineOutputArtifact]: ...
    region: builtins.str
    role_arn: builtins.str
    run_order: builtins.int
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        action_type_id: global___PipelineActionTypeId | None = ...,
        configuration: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        input_artifacts: collections.abc.Iterable[global___PipelineInputArtifact] | None = ...,
        name: builtins.str = ...,
        namespace: builtins.str = ...,
        output_artifacts: collections.abc.Iterable[global___PipelineOutputArtifact] | None = ...,
        region: builtins.str = ...,
        role_arn: builtins.str = ...,
        run_order: builtins.int = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["action_type_id", b"action_type_id", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["action_type_id", b"action_type_id", "configuration", b"configuration", "input_artifacts", b"input_artifacts", "name", b"name", "namespace", b"namespace", "output_artifacts", b"output_artifacts", "region", b"region", "resource_info", b"resource_info", "role_arn", b"role_arn", "run_order", b"run_order"]) -> None: ...

global___PipelineActionDeclaration = PipelineActionDeclaration

@typing_extensions.final
class PipelineBlockerDeclaration(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    name: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        name: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "resource_info", b"resource_info"]) -> None: ...

global___PipelineBlockerDeclaration = PipelineBlockerDeclaration

@typing_extensions.final
class PipelineStageDeclaration(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    ACTIONS_FIELD_NUMBER: builtins.int
    BLOCKERS_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def actions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___PipelineActionDeclaration]: ...
    @property
    def blockers(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___PipelineBlockerDeclaration]: ...
    name: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        actions: collections.abc.Iterable[global___PipelineActionDeclaration] | None = ...,
        blockers: collections.abc.Iterable[global___PipelineBlockerDeclaration] | None = ...,
        name: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["actions", b"actions", "blockers", b"blockers", "name", b"name", "resource_info", b"resource_info"]) -> None: ...

global___PipelineStageDeclaration = PipelineStageDeclaration

@typing_extensions.final
class Pipeline(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class TagsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.str
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    ARTIFACT_STORE_FIELD_NUMBER: builtins.int
    ARTIFACT_STORES_FIELD_NUMBER: builtins.int
    DISABLE_INBOUND_STAGE_TRANSITIONS_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    RESTART_EXECUTION_ON_UPDATE_FIELD_NUMBER: builtins.int
    ROLE_ARN_FIELD_NUMBER: builtins.int
    STAGES_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def artifact_store(self) -> global___PipelineArtifactStore: ...
    @property
    def artifact_stores(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___PipelineArtifactStoreMap]: ...
    @property
    def disable_inbound_stage_transitions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___PipelineStageTransition]: ...
    name: builtins.str
    restart_execution_on_update: builtins.bool
    role_arn: builtins.str
    @property
    def stages(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___PipelineStageDeclaration]: ...
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        artifact_store: global___PipelineArtifactStore | None = ...,
        artifact_stores: collections.abc.Iterable[global___PipelineArtifactStoreMap] | None = ...,
        disable_inbound_stage_transitions: collections.abc.Iterable[global___PipelineStageTransition] | None = ...,
        name: builtins.str = ...,
        restart_execution_on_update: builtins.bool = ...,
        role_arn: builtins.str = ...,
        stages: collections.abc.Iterable[global___PipelineStageDeclaration] | None = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["artifact_store", b"artifact_store", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["artifact_store", b"artifact_store", "artifact_stores", b"artifact_stores", "disable_inbound_stage_transitions", b"disable_inbound_stage_transitions", "name", b"name", "resource_info", b"resource_info", "restart_execution_on_update", b"restart_execution_on_update", "role_arn", b"role_arn", "stages", b"stages", "tags", b"tags"]) -> None: ...

global___Pipeline = Pipeline

@typing_extensions.final
class WebhookWebhookAuthConfiguration(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    ALLOWED_IP_RANGE_FIELD_NUMBER: builtins.int
    SECRET_TOKEN_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    allowed_ip_range: builtins.str
    secret_token: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        allowed_ip_range: builtins.str = ...,
        secret_token: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["allowed_ip_range", b"allowed_ip_range", "resource_info", b"resource_info", "secret_token", b"secret_token"]) -> None: ...

global___WebhookWebhookAuthConfiguration = WebhookWebhookAuthConfiguration

@typing_extensions.final
class WebhookWebhookFilterRule(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    JSON_PATH_FIELD_NUMBER: builtins.int
    MATCH_EQUALS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    json_path: builtins.str
    match_equals: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        json_path: builtins.str = ...,
        match_equals: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["json_path", b"json_path", "match_equals", b"match_equals", "resource_info", b"resource_info"]) -> None: ...

global___WebhookWebhookFilterRule = WebhookWebhookFilterRule

@typing_extensions.final
class Webhook(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    AUTHENTICATION_CONFIGURATION_FIELD_NUMBER: builtins.int
    FILTERS_FIELD_NUMBER: builtins.int
    AUTHENTICATION_FIELD_NUMBER: builtins.int
    TARGET_PIPELINE_FIELD_NUMBER: builtins.int
    TARGET_ACTION_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    TARGET_PIPELINE_VERSION_FIELD_NUMBER: builtins.int
    REGISTER_WITH_THIRD_PARTY_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def authentication_configuration(self) -> global___WebhookWebhookAuthConfiguration: ...
    @property
    def filters(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___WebhookWebhookFilterRule]: ...
    authentication: builtins.str
    target_pipeline: builtins.str
    target_action: builtins.str
    name: builtins.str
    target_pipeline_version: builtins.int
    register_with_third_party: builtins.bool
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        authentication_configuration: global___WebhookWebhookAuthConfiguration | None = ...,
        filters: collections.abc.Iterable[global___WebhookWebhookFilterRule] | None = ...,
        authentication: builtins.str = ...,
        target_pipeline: builtins.str = ...,
        target_action: builtins.str = ...,
        name: builtins.str = ...,
        target_pipeline_version: builtins.int = ...,
        register_with_third_party: builtins.bool = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["authentication_configuration", b"authentication_configuration", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["authentication", b"authentication", "authentication_configuration", b"authentication_configuration", "filters", b"filters", "name", b"name", "register_with_third_party", b"register_with_third_party", "resource_info", b"resource_info", "target_action", b"target_action", "target_pipeline", b"target_pipeline", "target_pipeline_version", b"target_pipeline_version"]) -> None: ...

global___Webhook = Webhook
