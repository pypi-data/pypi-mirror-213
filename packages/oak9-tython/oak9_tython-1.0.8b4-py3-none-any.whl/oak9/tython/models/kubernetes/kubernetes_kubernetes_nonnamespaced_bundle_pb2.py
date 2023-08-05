# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: kubernetes/kubernetes_kubernetes_nonnamespaced_bundle.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oak9.tython.models.shared import shared_pb2 as shared_dot_shared__pb2
from oak9.tython.models.kubernetes.kubernetes_io.k8s.api.core import v1_pb2 as kubernetes_dot_kubernetes__io_dot_k8s_dot_api_dot_core_dot_v1__pb2
from oak9.tython.models.kubernetes.kubernetes_io.k8s.api.certificates import v1_pb2 as kubernetes_dot_kubernetes__io_dot_k8s_dot_api_dot_certificates_dot_v1__pb2
from oak9.tython.models.kubernetes.kubernetes_io.k8s.api.admissionregistration import v1_pb2 as kubernetes_dot_kubernetes__io_dot_k8s_dot_api_dot_admissionregistration_dot_v1__pb2
from oak9.tython.models.kubernetes.kubernetes_io.k8s.api.networking import v1_pb2 as kubernetes_dot_kubernetes__io_dot_k8s_dot_api_dot_networking_dot_v1__pb2
from oak9.tython.models.kubernetes.kubernetes_io.k8s.api.node import v1_pb2 as kubernetes_dot_kubernetes__io_dot_k8s_dot_api_dot_node_dot_v1__pb2
from oak9.tython.models.kubernetes.kubernetes_io.k8s.api.rbac import v1_pb2 as kubernetes_dot_kubernetes__io_dot_k8s_dot_api_dot_rbac_dot_v1__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n;kubernetes/kubernetes_kubernetes_nonnamespaced_bundle.proto\x12.sac_kubernetes.kubernetes_nonnamespaced_bundle\x1a\x13shared/shared.proto\x1a.kubernetes/kubernetes_io.k8s.api.core.v1.proto\x1a\x36kubernetes/kubernetes_io.k8s.api.certificates.v1.proto\x1a?kubernetes/kubernetes_io.k8s.api.admissionregistration.v1.proto\x1a\x34kubernetes/kubernetes_io.k8s.api.networking.v1.proto\x1a.kubernetes/kubernetes_io.k8s.api.node.v1.proto\x1a.kubernetes/kubernetes_io.k8s.api.rbac.v1.proto\"\x82\x07\n\x18Kubernetes_NonNamespaced\x12\x46\n\x10\x63omponent_status\x18\x01 \x03(\x0b\x32,.oak9.tython.k8s.api.core.v1.ComponentStatus\x12\x39\n\tnamespace\x18\x02 \x03(\x0b\x32&.oak9.tython.k8s.api.core.v1.Namespace\x12/\n\x04node\x18\x03 \x03(\x0b\x32!.oak9.tython.k8s.api.core.v1.Node\x12H\n\x11persistent_volume\x18\x04 \x03(\x0b\x32-.oak9.tython.k8s.api.core.v1.PersistentVolume\x12\x63\n\x1b\x63\x65rtificate_signing_request\x18\x05 \x03(\x0b\x32>.oak9.tython.k8s.api.certificates.v1.CertificateSigningRequest\x12r\n\x1emutating_webhook_configuration\x18\x06 \x03(\x0b\x32J.oak9.tython.k8s.api.admissionregistration.v1.MutatingWebhookConfiguration\x12v\n validating_webhook_configuration\x18\x07 \x03(\x0b\x32L.oak9.tython.k8s.api.admissionregistration.v1.ValidatingWebhookConfiguration\x12\x46\n\ringress_class\x18\x08 \x03(\x0b\x32/.oak9.tython.k8s.api.networking.v1.IngressClass\x12@\n\rruntime_class\x18\t \x03(\x0b\x32).oak9.tython.k8s.api.node.v1.RuntimeClass\x12M\n\x14\x63luster_role_binding\x18\n \x03(\x0b\x32/.oak9.tython.k8s.api.rbac.v1.ClusterRoleBinding\x12>\n\x0c\x63luster_role\x18\x0b \x03(\x0b\x32(.oak9.tython.k8s.api.rbac.v1.ClusterRoleb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'kubernetes.kubernetes_kubernetes_nonnamespaced_bundle_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _KUBERNETES_NONNAMESPACED._serialized_start=452
  _KUBERNETES_NONNAMESPACED._serialized_end=1350
# @@protoc_insertion_point(module_scope)
