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
class Microsoft_App(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONNECTED_ENVIRONMENTS_FIELD_NUMBER: builtins.int
    MANAGED_ENVIRONMENTS_FIELD_NUMBER: builtins.int
    @property
    def connected_environments(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ConnectedEnvironments]: ...
    @property
    def managed_environments(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ManagedEnvironments]: ...
    def __init__(
        self,
        *,
        connected_environments: collections.abc.Iterable[global___ConnectedEnvironments] | None = ...,
        managed_environments: collections.abc.Iterable[global___ManagedEnvironments] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["connected_environments", b"connected_environments", "managed_environments", b"managed_environments"]) -> None: ...

global___Microsoft_App = Microsoft_App

@typing_extensions.final
class ManagedEnvironmentsStorages(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    AZURE_FILE_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    name: builtins.str
    @property
    def azure_file(self) -> global___AzureFileProperties: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        name: builtins.str = ...,
        azure_file: global___AzureFileProperties | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["azure_file", b"azure_file", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["azure_file", b"azure_file", "name", b"name", "resource_info", b"resource_info"]) -> None: ...

global___ManagedEnvironmentsStorages = ManagedEnvironmentsStorages

@typing_extensions.final
class ManagedEnvironmentsDaprComponents(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    COMPONENT_TYPE_FIELD_NUMBER: builtins.int
    IGNORE_ERRORS_FIELD_NUMBER: builtins.int
    INIT_TIMEOUT_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    SCOPES_FIELD_NUMBER: builtins.int
    SECRETS_FIELD_NUMBER: builtins.int
    SECRET_STORE_COMPONENT_FIELD_NUMBER: builtins.int
    VERSION_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    name: builtins.str
    component_type: builtins.str
    ignore_errors: builtins.bool
    init_timeout: builtins.str
    @property
    def metadata(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DaprMetadata]: ...
    @property
    def scopes(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def secrets(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Secret]: ...
    secret_store_component: builtins.str
    version: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        name: builtins.str = ...,
        component_type: builtins.str = ...,
        ignore_errors: builtins.bool = ...,
        init_timeout: builtins.str = ...,
        metadata: collections.abc.Iterable[global___DaprMetadata] | None = ...,
        scopes: collections.abc.Iterable[builtins.str] | None = ...,
        secrets: collections.abc.Iterable[global___Secret] | None = ...,
        secret_store_component: builtins.str = ...,
        version: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["component_type", b"component_type", "ignore_errors", b"ignore_errors", "init_timeout", b"init_timeout", "metadata", b"metadata", "name", b"name", "resource_info", b"resource_info", "scopes", b"scopes", "secret_store_component", b"secret_store_component", "secrets", b"secrets", "version", b"version"]) -> None: ...

global___ManagedEnvironmentsDaprComponents = ManagedEnvironmentsDaprComponents

@typing_extensions.final
class ManagedEnvironmentsCertificates(google.protobuf.message.Message):
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
    LOCATION_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    PASSWORD_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    location: builtins.str
    name: builtins.str
    password: builtins.str
    value: builtins.str
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        location: builtins.str = ...,
        name: builtins.str = ...,
        password: builtins.str = ...,
        value: builtins.str = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["location", b"location", "name", b"name", "password", b"password", "resource_info", b"resource_info", "tags", b"tags", "value", b"value"]) -> None: ...

global___ManagedEnvironmentsCertificates = ManagedEnvironmentsCertificates

@typing_extensions.final
class ManagedEnvironments(google.protobuf.message.Message):
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
    LOCATION_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    APP_LOGS_CONFIGURATION_FIELD_NUMBER: builtins.int
    CUSTOM_DOMAIN_CONFIGURATION_FIELD_NUMBER: builtins.int
    DAPR_A_I_CONNECTION_STRING_FIELD_NUMBER: builtins.int
    DAPR_A_I_INSTRUMENTATION_KEY_FIELD_NUMBER: builtins.int
    VNET_CONFIGURATION_FIELD_NUMBER: builtins.int
    WORKLOAD_PROFILES_FIELD_NUMBER: builtins.int
    ZONE_REDUNDANT_FIELD_NUMBER: builtins.int
    SKU_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    MANAGED_ENVIRONMENTS_DAPR_COMPONENTS_FIELD_NUMBER: builtins.int
    MANAGED_ENVIRONMENTS_CERTIFICATES_FIELD_NUMBER: builtins.int
    MANAGED_ENVIRONMENTS_STORAGES_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    location: builtins.str
    name: builtins.str
    @property
    def app_logs_configuration(self) -> global___AppLogsConfiguration: ...
    @property
    def custom_domain_configuration(self) -> global___CustomDomainConfiguration: ...
    dapr_a_i_connection_string: builtins.str
    dapr_a_i_instrumentation_key: builtins.str
    @property
    def vnet_configuration(self) -> global___VnetConfiguration: ...
    @property
    def workload_profiles(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___WorkloadProfile]: ...
    zone_redundant: builtins.bool
    @property
    def sku(self) -> global___EnvironmentSkuProperties: ...
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    @property
    def managed_environments_dapr_components(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ManagedEnvironmentsDaprComponents]: ...
    @property
    def managed_environments_certificates(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ManagedEnvironmentsCertificates]: ...
    @property
    def managed_environments_storages(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ManagedEnvironmentsStorages]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        location: builtins.str = ...,
        name: builtins.str = ...,
        app_logs_configuration: global___AppLogsConfiguration | None = ...,
        custom_domain_configuration: global___CustomDomainConfiguration | None = ...,
        dapr_a_i_connection_string: builtins.str = ...,
        dapr_a_i_instrumentation_key: builtins.str = ...,
        vnet_configuration: global___VnetConfiguration | None = ...,
        workload_profiles: collections.abc.Iterable[global___WorkloadProfile] | None = ...,
        zone_redundant: builtins.bool = ...,
        sku: global___EnvironmentSkuProperties | None = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        managed_environments_dapr_components: collections.abc.Iterable[global___ManagedEnvironmentsDaprComponents] | None = ...,
        managed_environments_certificates: collections.abc.Iterable[global___ManagedEnvironmentsCertificates] | None = ...,
        managed_environments_storages: collections.abc.Iterable[global___ManagedEnvironmentsStorages] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["app_logs_configuration", b"app_logs_configuration", "custom_domain_configuration", b"custom_domain_configuration", "resource_info", b"resource_info", "sku", b"sku", "vnet_configuration", b"vnet_configuration"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["app_logs_configuration", b"app_logs_configuration", "custom_domain_configuration", b"custom_domain_configuration", "dapr_a_i_connection_string", b"dapr_a_i_connection_string", "dapr_a_i_instrumentation_key", b"dapr_a_i_instrumentation_key", "location", b"location", "managed_environments_certificates", b"managed_environments_certificates", "managed_environments_dapr_components", b"managed_environments_dapr_components", "managed_environments_storages", b"managed_environments_storages", "name", b"name", "resource_info", b"resource_info", "sku", b"sku", "tags", b"tags", "vnet_configuration", b"vnet_configuration", "workload_profiles", b"workload_profiles", "zone_redundant", b"zone_redundant"]) -> None: ...

global___ManagedEnvironments = ManagedEnvironments

@typing_extensions.final
class EnvironmentSkuProperties(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    name: builtins.str
    def __init__(
        self,
        *,
        name: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name"]) -> None: ...

global___EnvironmentSkuProperties = EnvironmentSkuProperties

@typing_extensions.final
class WorkloadProfile(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MAXIMUM_COUNT_FIELD_NUMBER: builtins.int
    MINIMUM_COUNT_FIELD_NUMBER: builtins.int
    WORKLOAD_PROFILE_TYPE_FIELD_NUMBER: builtins.int
    maximum_count: builtins.int
    minimum_count: builtins.int
    workload_profile_type: builtins.str
    def __init__(
        self,
        *,
        maximum_count: builtins.int = ...,
        minimum_count: builtins.int = ...,
        workload_profile_type: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["maximum_count", b"maximum_count", "minimum_count", b"minimum_count", "workload_profile_type", b"workload_profile_type"]) -> None: ...

global___WorkloadProfile = WorkloadProfile

@typing_extensions.final
class VnetConfiguration(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DOCKER_BRIDGE_CIDR_FIELD_NUMBER: builtins.int
    INFRASTRUCTURE_SUBNET_ID_FIELD_NUMBER: builtins.int
    INTERNAL_FIELD_NUMBER: builtins.int
    OUTBOUND_SETTINGS_FIELD_NUMBER: builtins.int
    PLATFORM_RESERVED_CIDR_FIELD_NUMBER: builtins.int
    PLATFORM_RESERVED_DNS_IP_FIELD_NUMBER: builtins.int
    RUNTIME_SUBNET_ID_FIELD_NUMBER: builtins.int
    docker_bridge_cidr: builtins.str
    infrastructure_subnet_id: builtins.str
    internal: builtins.bool
    @property
    def outbound_settings(self) -> global___ManagedEnvironmentOutboundSettings: ...
    platform_reserved_cidr: builtins.str
    platform_reserved_dns_ip: builtins.str
    runtime_subnet_id: builtins.str
    def __init__(
        self,
        *,
        docker_bridge_cidr: builtins.str = ...,
        infrastructure_subnet_id: builtins.str = ...,
        internal: builtins.bool = ...,
        outbound_settings: global___ManagedEnvironmentOutboundSettings | None = ...,
        platform_reserved_cidr: builtins.str = ...,
        platform_reserved_dns_ip: builtins.str = ...,
        runtime_subnet_id: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["outbound_settings", b"outbound_settings"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["docker_bridge_cidr", b"docker_bridge_cidr", "infrastructure_subnet_id", b"infrastructure_subnet_id", "internal", b"internal", "outbound_settings", b"outbound_settings", "platform_reserved_cidr", b"platform_reserved_cidr", "platform_reserved_dns_ip", b"platform_reserved_dns_ip", "runtime_subnet_id", b"runtime_subnet_id"]) -> None: ...

global___VnetConfiguration = VnetConfiguration

@typing_extensions.final
class ManagedEnvironmentOutboundSettings(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    OUT_BOUND_TYPE_FIELD_NUMBER: builtins.int
    VIRTUAL_NETWORK_APPLIANCE_IP_FIELD_NUMBER: builtins.int
    out_bound_type: builtins.str
    virtual_network_appliance_ip: builtins.str
    def __init__(
        self,
        *,
        out_bound_type: builtins.str = ...,
        virtual_network_appliance_ip: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["out_bound_type", b"out_bound_type", "virtual_network_appliance_ip", b"virtual_network_appliance_ip"]) -> None: ...

global___ManagedEnvironmentOutboundSettings = ManagedEnvironmentOutboundSettings

@typing_extensions.final
class AppLogsConfiguration(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DESTINATION_FIELD_NUMBER: builtins.int
    LOG_ANALYTICS_CONFIGURATION_FIELD_NUMBER: builtins.int
    destination: builtins.str
    @property
    def log_analytics_configuration(self) -> global___LogAnalyticsConfiguration: ...
    def __init__(
        self,
        *,
        destination: builtins.str = ...,
        log_analytics_configuration: global___LogAnalyticsConfiguration | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["log_analytics_configuration", b"log_analytics_configuration"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["destination", b"destination", "log_analytics_configuration", b"log_analytics_configuration"]) -> None: ...

global___AppLogsConfiguration = AppLogsConfiguration

@typing_extensions.final
class LogAnalyticsConfiguration(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CUSTOMER_ID_FIELD_NUMBER: builtins.int
    SHARED_KEY_FIELD_NUMBER: builtins.int
    customer_id: builtins.str
    shared_key: builtins.str
    def __init__(
        self,
        *,
        customer_id: builtins.str = ...,
        shared_key: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["customer_id", b"customer_id", "shared_key", b"shared_key"]) -> None: ...

global___LogAnalyticsConfiguration = LogAnalyticsConfiguration

@typing_extensions.final
class ConnectedEnvironmentsStorages(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    AZURE_FILE_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    name: builtins.str
    @property
    def azure_file(self) -> global___AzureFileProperties: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        name: builtins.str = ...,
        azure_file: global___AzureFileProperties | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["azure_file", b"azure_file", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["azure_file", b"azure_file", "name", b"name", "resource_info", b"resource_info"]) -> None: ...

global___ConnectedEnvironmentsStorages = ConnectedEnvironmentsStorages

@typing_extensions.final
class AzureFileProperties(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ACCESS_MODE_FIELD_NUMBER: builtins.int
    ACCOUNT_KEY_FIELD_NUMBER: builtins.int
    ACCOUNT_NAME_FIELD_NUMBER: builtins.int
    SHARE_NAME_FIELD_NUMBER: builtins.int
    access_mode: builtins.str
    account_key: builtins.str
    account_name: builtins.str
    share_name: builtins.str
    def __init__(
        self,
        *,
        access_mode: builtins.str = ...,
        account_key: builtins.str = ...,
        account_name: builtins.str = ...,
        share_name: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["access_mode", b"access_mode", "account_key", b"account_key", "account_name", b"account_name", "share_name", b"share_name"]) -> None: ...

global___AzureFileProperties = AzureFileProperties

@typing_extensions.final
class ConnectedEnvironmentsDaprComponents(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    COMPONENT_TYPE_FIELD_NUMBER: builtins.int
    IGNORE_ERRORS_FIELD_NUMBER: builtins.int
    INIT_TIMEOUT_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    SCOPES_FIELD_NUMBER: builtins.int
    SECRETS_FIELD_NUMBER: builtins.int
    SECRET_STORE_COMPONENT_FIELD_NUMBER: builtins.int
    VERSION_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    name: builtins.str
    component_type: builtins.str
    ignore_errors: builtins.bool
    init_timeout: builtins.str
    @property
    def metadata(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DaprMetadata]: ...
    @property
    def scopes(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def secrets(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Secret]: ...
    secret_store_component: builtins.str
    version: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        name: builtins.str = ...,
        component_type: builtins.str = ...,
        ignore_errors: builtins.bool = ...,
        init_timeout: builtins.str = ...,
        metadata: collections.abc.Iterable[global___DaprMetadata] | None = ...,
        scopes: collections.abc.Iterable[builtins.str] | None = ...,
        secrets: collections.abc.Iterable[global___Secret] | None = ...,
        secret_store_component: builtins.str = ...,
        version: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["component_type", b"component_type", "ignore_errors", b"ignore_errors", "init_timeout", b"init_timeout", "metadata", b"metadata", "name", b"name", "resource_info", b"resource_info", "scopes", b"scopes", "secret_store_component", b"secret_store_component", "secrets", b"secrets", "version", b"version"]) -> None: ...

global___ConnectedEnvironmentsDaprComponents = ConnectedEnvironmentsDaprComponents

@typing_extensions.final
class Secret(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    name: builtins.str
    value: builtins.str
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        value: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "value", b"value"]) -> None: ...

global___Secret = Secret

@typing_extensions.final
class DaprMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    SECRET_REF_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    name: builtins.str
    secret_ref: builtins.str
    value: builtins.str
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        secret_ref: builtins.str = ...,
        value: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "secret_ref", b"secret_ref", "value", b"value"]) -> None: ...

global___DaprMetadata = DaprMetadata

@typing_extensions.final
class ConnectedEnvironmentsCertificates(google.protobuf.message.Message):
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
    LOCATION_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    PASSWORD_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    location: builtins.str
    name: builtins.str
    password: builtins.str
    value: builtins.str
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        location: builtins.str = ...,
        name: builtins.str = ...,
        password: builtins.str = ...,
        value: builtins.str = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["location", b"location", "name", b"name", "password", b"password", "resource_info", b"resource_info", "tags", b"tags", "value", b"value"]) -> None: ...

global___ConnectedEnvironmentsCertificates = ConnectedEnvironmentsCertificates

@typing_extensions.final
class ConnectedEnvironments(google.protobuf.message.Message):
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
    EXTENDED_LOCATION_FIELD_NUMBER: builtins.int
    LOCATION_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    CUSTOM_DOMAIN_CONFIGURATION_FIELD_NUMBER: builtins.int
    DAPR_A_I_CONNECTION_STRING_FIELD_NUMBER: builtins.int
    STATIC_IP_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    CONNECTED_ENVIRONMENTS_CERTIFICATES_FIELD_NUMBER: builtins.int
    CONNECTED_ENVIRONMENTS_DAPR_COMPONENTS_FIELD_NUMBER: builtins.int
    CONNECTED_ENVIRONMENTS_STORAGES_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def extended_location(self) -> global___ExtendedLocation: ...
    location: builtins.str
    name: builtins.str
    @property
    def custom_domain_configuration(self) -> global___CustomDomainConfiguration: ...
    dapr_a_i_connection_string: builtins.str
    static_ip: builtins.str
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    @property
    def connected_environments_certificates(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ConnectedEnvironmentsCertificates]: ...
    @property
    def connected_environments_dapr_components(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ConnectedEnvironmentsDaprComponents]: ...
    @property
    def connected_environments_storages(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ConnectedEnvironmentsStorages]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        extended_location: global___ExtendedLocation | None = ...,
        location: builtins.str = ...,
        name: builtins.str = ...,
        custom_domain_configuration: global___CustomDomainConfiguration | None = ...,
        dapr_a_i_connection_string: builtins.str = ...,
        static_ip: builtins.str = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        connected_environments_certificates: collections.abc.Iterable[global___ConnectedEnvironmentsCertificates] | None = ...,
        connected_environments_dapr_components: collections.abc.Iterable[global___ConnectedEnvironmentsDaprComponents] | None = ...,
        connected_environments_storages: collections.abc.Iterable[global___ConnectedEnvironmentsStorages] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["custom_domain_configuration", b"custom_domain_configuration", "extended_location", b"extended_location", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["connected_environments_certificates", b"connected_environments_certificates", "connected_environments_dapr_components", b"connected_environments_dapr_components", "connected_environments_storages", b"connected_environments_storages", "custom_domain_configuration", b"custom_domain_configuration", "dapr_a_i_connection_string", b"dapr_a_i_connection_string", "extended_location", b"extended_location", "location", b"location", "name", b"name", "resource_info", b"resource_info", "static_ip", b"static_ip", "tags", b"tags"]) -> None: ...

global___ConnectedEnvironments = ConnectedEnvironments

@typing_extensions.final
class CustomDomainConfiguration(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CERTIFICATE_PASSWORD_FIELD_NUMBER: builtins.int
    CERTIFICATE_VALUE_FIELD_NUMBER: builtins.int
    DNS_SUFFIX_FIELD_NUMBER: builtins.int
    certificate_password: builtins.str
    certificate_value: builtins.str
    dns_suffix: builtins.str
    def __init__(
        self,
        *,
        certificate_password: builtins.str = ...,
        certificate_value: builtins.str = ...,
        dns_suffix: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["certificate_password", b"certificate_password", "certificate_value", b"certificate_value", "dns_suffix", b"dns_suffix"]) -> None: ...

global___CustomDomainConfiguration = CustomDomainConfiguration

@typing_extensions.final
class ExtendedLocation(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    name: builtins.str
    type: builtins.str
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        type: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "type", b"type"]) -> None: ...

global___ExtendedLocation = ExtendedLocation
