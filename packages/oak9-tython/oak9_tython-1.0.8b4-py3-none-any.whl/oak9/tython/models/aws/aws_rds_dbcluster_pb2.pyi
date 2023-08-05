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
class DBClusterDBClusterRole(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    FEATURE_NAME_FIELD_NUMBER: builtins.int
    ROLE_ARN_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    feature_name: builtins.str
    role_arn: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        feature_name: builtins.str = ...,
        role_arn: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["feature_name", b"feature_name", "resource_info", b"resource_info", "role_arn", b"role_arn"]) -> None: ...

global___DBClusterDBClusterRole = DBClusterDBClusterRole

@typing_extensions.final
class DBClusterScalingConfiguration(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    AUTO_PAUSE_FIELD_NUMBER: builtins.int
    MAX_CAPACITY_FIELD_NUMBER: builtins.int
    MIN_CAPACITY_FIELD_NUMBER: builtins.int
    SECONDS_UNTIL_AUTO_PAUSE_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    auto_pause: builtins.bool
    max_capacity: builtins.int
    min_capacity: builtins.int
    seconds_until_auto_pause: builtins.int
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        auto_pause: builtins.bool = ...,
        max_capacity: builtins.int = ...,
        min_capacity: builtins.int = ...,
        seconds_until_auto_pause: builtins.int = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["auto_pause", b"auto_pause", "max_capacity", b"max_capacity", "min_capacity", b"min_capacity", "resource_info", b"resource_info", "seconds_until_auto_pause", b"seconds_until_auto_pause"]) -> None: ...

global___DBClusterScalingConfiguration = DBClusterScalingConfiguration

@typing_extensions.final
class DBCluster(google.protobuf.message.Message):
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
    ASSOCIATED_ROLES_FIELD_NUMBER: builtins.int
    AVAILABILITY_ZONES_FIELD_NUMBER: builtins.int
    BACKTRACK_WINDOW_FIELD_NUMBER: builtins.int
    BACKUP_RETENTION_PERIOD_FIELD_NUMBER: builtins.int
    DB_CLUSTER_IDENTIFIER_FIELD_NUMBER: builtins.int
    DB_CLUSTER_PARAMETER_GROUP_NAME_FIELD_NUMBER: builtins.int
    DB_SUBNET_GROUP_NAME_FIELD_NUMBER: builtins.int
    DATABASE_NAME_FIELD_NUMBER: builtins.int
    DELETION_PROTECTION_FIELD_NUMBER: builtins.int
    ENABLE_CLOUDWATCH_LOGS_EXPORTS_FIELD_NUMBER: builtins.int
    ENABLE_HTTP_ENDPOINT_FIELD_NUMBER: builtins.int
    ENABLE_IAM_DATABASE_AUTHENTICATION_FIELD_NUMBER: builtins.int
    ENGINE_FIELD_NUMBER: builtins.int
    ENGINE_MODE_FIELD_NUMBER: builtins.int
    ENGINE_VERSION_FIELD_NUMBER: builtins.int
    KMS_KEY_ID_FIELD_NUMBER: builtins.int
    MASTER_USER_PASSWORD_FIELD_NUMBER: builtins.int
    MASTER_USERNAME_FIELD_NUMBER: builtins.int
    PORT_FIELD_NUMBER: builtins.int
    PREFERRED_BACKUP_WINDOW_FIELD_NUMBER: builtins.int
    PREFERRED_MAINTENANCE_WINDOW_FIELD_NUMBER: builtins.int
    REPLICATION_SOURCE_IDENTIFIER_FIELD_NUMBER: builtins.int
    RESTORE_TYPE_FIELD_NUMBER: builtins.int
    SCALING_CONFIGURATION_FIELD_NUMBER: builtins.int
    SNAPSHOT_IDENTIFIER_FIELD_NUMBER: builtins.int
    SOURCE_DB_CLUSTER_IDENTIFIER_FIELD_NUMBER: builtins.int
    SOURCE_REGION_FIELD_NUMBER: builtins.int
    STORAGE_ENCRYPTED_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    USE_LATEST_RESTORABLE_TIME_FIELD_NUMBER: builtins.int
    VPC_SECURITY_GROUP_IDS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def associated_roles(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DBClusterDBClusterRole]: ...
    @property
    def availability_zones(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    backtrack_window: builtins.int
    backup_retention_period: builtins.int
    db_cluster_identifier: builtins.str
    db_cluster_parameter_group_name: builtins.str
    db_subnet_group_name: builtins.str
    database_name: builtins.str
    deletion_protection: builtins.bool
    @property
    def enable_cloudwatch_logs_exports(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    enable_http_endpoint: builtins.bool
    enable_iam_database_authentication: builtins.bool
    engine: builtins.str
    engine_mode: builtins.str
    engine_version: builtins.str
    kms_key_id: builtins.str
    master_user_password: builtins.str
    master_username: builtins.str
    port: builtins.int
    preferred_backup_window: builtins.str
    preferred_maintenance_window: builtins.str
    replication_source_identifier: builtins.str
    restore_type: builtins.str
    @property
    def scaling_configuration(self) -> global___DBClusterScalingConfiguration: ...
    snapshot_identifier: builtins.str
    source_db_cluster_identifier: builtins.str
    source_region: builtins.str
    storage_encrypted: builtins.bool
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    use_latest_restorable_time: builtins.bool
    @property
    def vpc_security_group_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        associated_roles: collections.abc.Iterable[global___DBClusterDBClusterRole] | None = ...,
        availability_zones: collections.abc.Iterable[builtins.str] | None = ...,
        backtrack_window: builtins.int = ...,
        backup_retention_period: builtins.int = ...,
        db_cluster_identifier: builtins.str = ...,
        db_cluster_parameter_group_name: builtins.str = ...,
        db_subnet_group_name: builtins.str = ...,
        database_name: builtins.str = ...,
        deletion_protection: builtins.bool = ...,
        enable_cloudwatch_logs_exports: collections.abc.Iterable[builtins.str] | None = ...,
        enable_http_endpoint: builtins.bool = ...,
        enable_iam_database_authentication: builtins.bool = ...,
        engine: builtins.str = ...,
        engine_mode: builtins.str = ...,
        engine_version: builtins.str = ...,
        kms_key_id: builtins.str = ...,
        master_user_password: builtins.str = ...,
        master_username: builtins.str = ...,
        port: builtins.int = ...,
        preferred_backup_window: builtins.str = ...,
        preferred_maintenance_window: builtins.str = ...,
        replication_source_identifier: builtins.str = ...,
        restore_type: builtins.str = ...,
        scaling_configuration: global___DBClusterScalingConfiguration | None = ...,
        snapshot_identifier: builtins.str = ...,
        source_db_cluster_identifier: builtins.str = ...,
        source_region: builtins.str = ...,
        storage_encrypted: builtins.bool = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        use_latest_restorable_time: builtins.bool = ...,
        vpc_security_group_ids: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info", "scaling_configuration", b"scaling_configuration"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["associated_roles", b"associated_roles", "availability_zones", b"availability_zones", "backtrack_window", b"backtrack_window", "backup_retention_period", b"backup_retention_period", "database_name", b"database_name", "db_cluster_identifier", b"db_cluster_identifier", "db_cluster_parameter_group_name", b"db_cluster_parameter_group_name", "db_subnet_group_name", b"db_subnet_group_name", "deletion_protection", b"deletion_protection", "enable_cloudwatch_logs_exports", b"enable_cloudwatch_logs_exports", "enable_http_endpoint", b"enable_http_endpoint", "enable_iam_database_authentication", b"enable_iam_database_authentication", "engine", b"engine", "engine_mode", b"engine_mode", "engine_version", b"engine_version", "kms_key_id", b"kms_key_id", "master_user_password", b"master_user_password", "master_username", b"master_username", "port", b"port", "preferred_backup_window", b"preferred_backup_window", "preferred_maintenance_window", b"preferred_maintenance_window", "replication_source_identifier", b"replication_source_identifier", "resource_info", b"resource_info", "restore_type", b"restore_type", "scaling_configuration", b"scaling_configuration", "snapshot_identifier", b"snapshot_identifier", "source_db_cluster_identifier", b"source_db_cluster_identifier", "source_region", b"source_region", "storage_encrypted", b"storage_encrypted", "tags", b"tags", "use_latest_restorable_time", b"use_latest_restorable_time", "vpc_security_group_ids", b"vpc_security_group_ids"]) -> None: ...

global___DBCluster = DBCluster

@typing_extensions.final
class RDS_DBCluster(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DB_CLUSTER_FIELD_NUMBER: builtins.int
    DB_CLUSTER_PARAMETER_GROUP_FIELD_NUMBER: builtins.int
    DB_PROXY_FIELD_NUMBER: builtins.int
    DB_PROXY_TARGET_GROUP_FIELD_NUMBER: builtins.int
    DB_SECURITY_GROUP_FIELD_NUMBER: builtins.int
    DB_SECURITY_GROUP_INGRESS_FIELD_NUMBER: builtins.int
    DB_SUBNET_GROUP_FIELD_NUMBER: builtins.int
    EVENT_SUBSCRIPTION_FIELD_NUMBER: builtins.int
    OPTION_GROUP_FIELD_NUMBER: builtins.int
    @property
    def db_cluster(self) -> global___DBCluster: ...
    @property
    def db_cluster_parameter_group(self) -> global___DBClusterParameterGroup: ...
    @property
    def db_proxy(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DBProxy]: ...
    @property
    def db_proxy_target_group(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DBProxyTargetGroup]: ...
    @property
    def db_security_group(self) -> global___DBSecurityGroup: ...
    @property
    def db_security_group_ingress(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DBSecurityGroupIngress]: ...
    @property
    def db_subnet_group(self) -> global___DBSubnetGroup: ...
    @property
    def event_subscription(self) -> global___EventSubscription: ...
    @property
    def option_group(self) -> global___OptionGroup: ...
    def __init__(
        self,
        *,
        db_cluster: global___DBCluster | None = ...,
        db_cluster_parameter_group: global___DBClusterParameterGroup | None = ...,
        db_proxy: collections.abc.Iterable[global___DBProxy] | None = ...,
        db_proxy_target_group: collections.abc.Iterable[global___DBProxyTargetGroup] | None = ...,
        db_security_group: global___DBSecurityGroup | None = ...,
        db_security_group_ingress: collections.abc.Iterable[global___DBSecurityGroupIngress] | None = ...,
        db_subnet_group: global___DBSubnetGroup | None = ...,
        event_subscription: global___EventSubscription | None = ...,
        option_group: global___OptionGroup | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["db_cluster", b"db_cluster", "db_cluster_parameter_group", b"db_cluster_parameter_group", "db_security_group", b"db_security_group", "db_subnet_group", b"db_subnet_group", "event_subscription", b"event_subscription", "option_group", b"option_group"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["db_cluster", b"db_cluster", "db_cluster_parameter_group", b"db_cluster_parameter_group", "db_proxy", b"db_proxy", "db_proxy_target_group", b"db_proxy_target_group", "db_security_group", b"db_security_group", "db_security_group_ingress", b"db_security_group_ingress", "db_subnet_group", b"db_subnet_group", "event_subscription", b"event_subscription", "option_group", b"option_group"]) -> None: ...

global___RDS_DBCluster = RDS_DBCluster

@typing_extensions.final
class DBClusterParameterGroup(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class ParametersEntry(google.protobuf.message.Message):
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
    DESCRIPTION_FIELD_NUMBER: builtins.int
    FAMILY_FIELD_NUMBER: builtins.int
    PARAMETERS_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    description: builtins.str
    family: builtins.str
    @property
    def parameters(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        description: builtins.str = ...,
        family: builtins.str = ...,
        parameters: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["description", b"description", "family", b"family", "parameters", b"parameters", "resource_info", b"resource_info", "tags", b"tags"]) -> None: ...

global___DBClusterParameterGroup = DBClusterParameterGroup

@typing_extensions.final
class DBProxyTagFormat(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    KEY_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    key: builtins.str
    value: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        key: builtins.str = ...,
        value: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "resource_info", b"resource_info", "value", b"value"]) -> None: ...

global___DBProxyTagFormat = DBProxyTagFormat

@typing_extensions.final
class DBProxy(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    DB_PROXY_NAME_FIELD_NUMBER: builtins.int
    DEBUG_LOGGING_FIELD_NUMBER: builtins.int
    ENGINE_FAMILY_FIELD_NUMBER: builtins.int
    IDLE_CLIENT_TIMEOUT_FIELD_NUMBER: builtins.int
    REQUIRE_TLS_FIELD_NUMBER: builtins.int
    ROLE_ARN_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    VPC_SECURITY_GROUP_IDS_FIELD_NUMBER: builtins.int
    VPC_SUBNET_IDS_FIELD_NUMBER: builtins.int
    AUTH_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    db_proxy_name: builtins.str
    debug_logging: builtins.bool
    engine_family: builtins.str
    idle_client_timeout: builtins.int
    require_tls: builtins.bool
    role_arn: builtins.str
    @property
    def tags(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DBProxyTagFormat]: ...
    @property
    def vpc_security_group_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def vpc_subnet_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def auth(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DBProxyAuth]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        db_proxy_name: builtins.str = ...,
        debug_logging: builtins.bool = ...,
        engine_family: builtins.str = ...,
        idle_client_timeout: builtins.int = ...,
        require_tls: builtins.bool = ...,
        role_arn: builtins.str = ...,
        tags: collections.abc.Iterable[global___DBProxyTagFormat] | None = ...,
        vpc_security_group_ids: collections.abc.Iterable[builtins.str] | None = ...,
        vpc_subnet_ids: collections.abc.Iterable[builtins.str] | None = ...,
        auth: collections.abc.Iterable[global___DBProxyAuth] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["auth", b"auth", "db_proxy_name", b"db_proxy_name", "debug_logging", b"debug_logging", "engine_family", b"engine_family", "idle_client_timeout", b"idle_client_timeout", "require_tls", b"require_tls", "resource_info", b"resource_info", "role_arn", b"role_arn", "tags", b"tags", "vpc_security_group_ids", b"vpc_security_group_ids", "vpc_subnet_ids", b"vpc_subnet_ids"]) -> None: ...

global___DBProxy = DBProxy

@typing_extensions.final
class DBProxyTargetGroupConnectionPoolConfigurationInfoFormat(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    MAX_CONNECTIONS_PERCENT_FIELD_NUMBER: builtins.int
    MAX_IDLE_CONNECTIONS_PERCENT_FIELD_NUMBER: builtins.int
    CONNECTION_BORROW_TIMEOUT_FIELD_NUMBER: builtins.int
    SESSION_PINNING_FILTERS_FIELD_NUMBER: builtins.int
    INIT_QUERY_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    max_connections_percent: builtins.int
    max_idle_connections_percent: builtins.int
    connection_borrow_timeout: builtins.int
    @property
    def session_pinning_filters(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    init_query: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        max_connections_percent: builtins.int = ...,
        max_idle_connections_percent: builtins.int = ...,
        connection_borrow_timeout: builtins.int = ...,
        session_pinning_filters: collections.abc.Iterable[builtins.str] | None = ...,
        init_query: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["connection_borrow_timeout", b"connection_borrow_timeout", "init_query", b"init_query", "max_connections_percent", b"max_connections_percent", "max_idle_connections_percent", b"max_idle_connections_percent", "resource_info", b"resource_info", "session_pinning_filters", b"session_pinning_filters"]) -> None: ...

global___DBProxyTargetGroupConnectionPoolConfigurationInfoFormat = DBProxyTargetGroupConnectionPoolConfigurationInfoFormat

@typing_extensions.final
class DBProxyTargetGroup(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    DB_PROXY_NAME_FIELD_NUMBER: builtins.int
    TARGET_GROUP_NAME_FIELD_NUMBER: builtins.int
    CONNECTION_POOL_CONFIGURATION_INFO_FIELD_NUMBER: builtins.int
    DB_INSTANCE_IDENTIFIERS_FIELD_NUMBER: builtins.int
    DB_CLUSTER_IDENTIFIERS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    db_proxy_name: builtins.str
    target_group_name: builtins.str
    @property
    def connection_pool_configuration_info(self) -> global___DBProxyTargetGroupConnectionPoolConfigurationInfoFormat: ...
    @property
    def db_instance_identifiers(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def db_cluster_identifiers(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        db_proxy_name: builtins.str = ...,
        target_group_name: builtins.str = ...,
        connection_pool_configuration_info: global___DBProxyTargetGroupConnectionPoolConfigurationInfoFormat | None = ...,
        db_instance_identifiers: collections.abc.Iterable[builtins.str] | None = ...,
        db_cluster_identifiers: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["connection_pool_configuration_info", b"connection_pool_configuration_info", "resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["connection_pool_configuration_info", b"connection_pool_configuration_info", "db_cluster_identifiers", b"db_cluster_identifiers", "db_instance_identifiers", b"db_instance_identifiers", "db_proxy_name", b"db_proxy_name", "resource_info", b"resource_info", "target_group_name", b"target_group_name"]) -> None: ...

global___DBProxyTargetGroup = DBProxyTargetGroup

@typing_extensions.final
class DBSecurityGroupIngress(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    CIDR_IP_FIELD_NUMBER: builtins.int
    E_C2_SECURITY_GROUP_ID_FIELD_NUMBER: builtins.int
    E_C2_SECURITY_GROUP_NAME_FIELD_NUMBER: builtins.int
    E_C2_SECURITY_GROUP_OWNER_ID_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    cidr_ip: builtins.str
    e_c2_security_group_id: builtins.str
    e_c2_security_group_name: builtins.str
    e_c2_security_group_owner_id: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        cidr_ip: builtins.str = ...,
        e_c2_security_group_id: builtins.str = ...,
        e_c2_security_group_name: builtins.str = ...,
        e_c2_security_group_owner_id: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["cidr_ip", b"cidr_ip", "e_c2_security_group_id", b"e_c2_security_group_id", "e_c2_security_group_name", b"e_c2_security_group_name", "e_c2_security_group_owner_id", b"e_c2_security_group_owner_id", "resource_info", b"resource_info"]) -> None: ...

global___DBSecurityGroupIngress = DBSecurityGroupIngress

@typing_extensions.final
class DBSecurityGroup(google.protobuf.message.Message):
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
    DB_SECURITY_GROUP_INGRESS_FIELD_NUMBER: builtins.int
    E_C2_VPC_ID_FIELD_NUMBER: builtins.int
    GROUP_DESCRIPTION_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def db_security_group_ingress(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DBSecurityGroupIngress]: ...
    e_c2_vpc_id: builtins.str
    group_description: builtins.str
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        db_security_group_ingress: collections.abc.Iterable[global___DBSecurityGroupIngress] | None = ...,
        e_c2_vpc_id: builtins.str = ...,
        group_description: builtins.str = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["db_security_group_ingress", b"db_security_group_ingress", "e_c2_vpc_id", b"e_c2_vpc_id", "group_description", b"group_description", "resource_info", b"resource_info", "tags", b"tags"]) -> None: ...

global___DBSecurityGroup = DBSecurityGroup

@typing_extensions.final
class DBSubnetGroup(google.protobuf.message.Message):
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
    DB_SUBNET_GROUP_DESCRIPTION_FIELD_NUMBER: builtins.int
    DB_SUBNET_GROUP_NAME_FIELD_NUMBER: builtins.int
    SUBNET_IDS_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    db_subnet_group_description: builtins.str
    db_subnet_group_name: builtins.str
    @property
    def subnet_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        db_subnet_group_description: builtins.str = ...,
        db_subnet_group_name: builtins.str = ...,
        subnet_ids: collections.abc.Iterable[builtins.str] | None = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["db_subnet_group_description", b"db_subnet_group_description", "db_subnet_group_name", b"db_subnet_group_name", "resource_info", b"resource_info", "subnet_ids", b"subnet_ids", "tags", b"tags"]) -> None: ...

global___DBSubnetGroup = DBSubnetGroup

@typing_extensions.final
class EventSubscription(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    ENABLED_FIELD_NUMBER: builtins.int
    EVENT_CATEGORIES_FIELD_NUMBER: builtins.int
    SNS_TOPIC_ARN_FIELD_NUMBER: builtins.int
    SOURCE_IDS_FIELD_NUMBER: builtins.int
    SOURCE_TYPE_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    enabled: builtins.bool
    @property
    def event_categories(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    sns_topic_arn: builtins.str
    @property
    def source_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    source_type: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        enabled: builtins.bool = ...,
        event_categories: collections.abc.Iterable[builtins.str] | None = ...,
        sns_topic_arn: builtins.str = ...,
        source_ids: collections.abc.Iterable[builtins.str] | None = ...,
        source_type: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["enabled", b"enabled", "event_categories", b"event_categories", "resource_info", b"resource_info", "sns_topic_arn", b"sns_topic_arn", "source_ids", b"source_ids", "source_type", b"source_type"]) -> None: ...

global___EventSubscription = EventSubscription

@typing_extensions.final
class OptionGroupOptionSetting(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    name: builtins.str
    value: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        name: builtins.str = ...,
        value: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "resource_info", b"resource_info", "value", b"value"]) -> None: ...

global___OptionGroupOptionSetting = OptionGroupOptionSetting

@typing_extensions.final
class OptionGroupOptionConfiguration(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    DB_SECURITY_GROUP_MEMBERSHIPS_FIELD_NUMBER: builtins.int
    OPTION_NAME_FIELD_NUMBER: builtins.int
    OPTION_SETTINGS_FIELD_NUMBER: builtins.int
    OPTION_VERSION_FIELD_NUMBER: builtins.int
    PORT_FIELD_NUMBER: builtins.int
    VPC_SECURITY_GROUP_MEMBERSHIPS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    @property
    def db_security_group_memberships(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    option_name: builtins.str
    @property
    def option_settings(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___OptionGroupOptionSetting]: ...
    option_version: builtins.str
    port: builtins.int
    @property
    def vpc_security_group_memberships(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        db_security_group_memberships: collections.abc.Iterable[builtins.str] | None = ...,
        option_name: builtins.str = ...,
        option_settings: collections.abc.Iterable[global___OptionGroupOptionSetting] | None = ...,
        option_version: builtins.str = ...,
        port: builtins.int = ...,
        vpc_security_group_memberships: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["db_security_group_memberships", b"db_security_group_memberships", "option_name", b"option_name", "option_settings", b"option_settings", "option_version", b"option_version", "port", b"port", "resource_info", b"resource_info", "vpc_security_group_memberships", b"vpc_security_group_memberships"]) -> None: ...

global___OptionGroupOptionConfiguration = OptionGroupOptionConfiguration

@typing_extensions.final
class DBProxyAuth(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_INFO_FIELD_NUMBER: builtins.int
    AUTH_SCHEME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    IAM_AUTH_FIELD_NUMBER: builtins.int
    SECRET_ARN_FIELD_NUMBER: builtins.int
    USER_NAME_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    auth_scheme: builtins.str
    description: builtins.str
    iam_auth: builtins.str
    secret_arn: builtins.str
    user_name: builtins.str
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        auth_scheme: builtins.str = ...,
        description: builtins.str = ...,
        iam_auth: builtins.str = ...,
        secret_arn: builtins.str = ...,
        user_name: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["auth_scheme", b"auth_scheme", "description", b"description", "iam_auth", b"iam_auth", "resource_info", b"resource_info", "secret_arn", b"secret_arn", "user_name", b"user_name"]) -> None: ...

global___DBProxyAuth = DBProxyAuth

@typing_extensions.final
class OptionGroup(google.protobuf.message.Message):
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
    ENGINE_NAME_FIELD_NUMBER: builtins.int
    MAJOR_ENGINE_VERSION_FIELD_NUMBER: builtins.int
    OPTION_CONFIGURATIONS_FIELD_NUMBER: builtins.int
    OPTION_GROUP_DESCRIPTION_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    @property
    def resource_info(self) -> shared.shared_pb2.ResourceInfo: ...
    engine_name: builtins.str
    major_engine_version: builtins.str
    @property
    def option_configurations(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___OptionGroupOptionConfiguration]: ...
    option_group_description: builtins.str
    @property
    def tags(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    def __init__(
        self,
        *,
        resource_info: shared.shared_pb2.ResourceInfo | None = ...,
        engine_name: builtins.str = ...,
        major_engine_version: builtins.str = ...,
        option_configurations: collections.abc.Iterable[global___OptionGroupOptionConfiguration] | None = ...,
        option_group_description: builtins.str = ...,
        tags: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_info", b"resource_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["engine_name", b"engine_name", "major_engine_version", b"major_engine_version", "option_configurations", b"option_configurations", "option_group_description", b"option_group_description", "resource_info", b"resource_info", "tags", b"tags"]) -> None: ...

global___OptionGroup = OptionGroup
