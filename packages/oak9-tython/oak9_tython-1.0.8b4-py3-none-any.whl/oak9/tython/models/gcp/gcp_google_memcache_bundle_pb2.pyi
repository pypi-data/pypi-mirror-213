"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import gcp.gcp_memcache_pb2
import google.protobuf.descriptor
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class GoogleMemcache(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MEMCACHE_INSTANCE_FIELD_NUMBER: builtins.int
    @property
    def memcache_instance(self) -> gcp.gcp_memcache_pb2.MemcacheInstance: ...
    def __init__(
        self,
        *,
        memcache_instance: gcp.gcp_memcache_pb2.MemcacheInstance | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["memcache_instance", b"memcache_instance"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["memcache_instance", b"memcache_instance"]) -> None: ...

global___GoogleMemcache = GoogleMemcache
