"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import gcp.gcp_dataflow_pb2
import google.protobuf.descriptor
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class GoogleDataflow(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DATAFLOW_JOB_FIELD_NUMBER: builtins.int
    @property
    def dataflow_job(self) -> gcp.gcp_dataflow_pb2.DataflowJob: ...
    def __init__(
        self,
        *,
        dataflow_job: gcp.gcp_dataflow_pb2.DataflowJob | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["dataflow_job", b"dataflow_job"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["dataflow_job", b"dataflow_job"]) -> None: ...

global___GoogleDataflow = GoogleDataflow
