# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ... import meta as _meta
from ._inputs import *

__all__ = ['ServiceAccountArgs', 'ServiceAccount']

@pulumi.input_type
class ServiceAccountArgs:
    def __init__(__self__, *,
                 api_version: Optional[pulumi.Input[str]] = None,
                 automount_service_account_token: Optional[pulumi.Input[bool]] = None,
                 image_pull_secrets: Optional[pulumi.Input[Sequence[pulumi.Input['LocalObjectReferenceArgs']]]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input['_meta.v1.ObjectMetaArgs']] = None,
                 secrets: Optional[pulumi.Input[Sequence[pulumi.Input['ObjectReferenceArgs']]]] = None):
        """
        The set of arguments for constructing a ServiceAccount resource.
        :param pulumi.Input[str] api_version: APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        :param pulumi.Input[bool] automount_service_account_token: AutomountServiceAccountToken indicates whether pods running as this service account should have an API token automatically mounted. Can be overridden at the pod level.
        :param pulumi.Input[Sequence[pulumi.Input['LocalObjectReferenceArgs']]] image_pull_secrets: ImagePullSecrets is a list of references to secrets in the same namespace to use for pulling any images in pods that reference this ServiceAccount. ImagePullSecrets are distinct from Secrets because Secrets can be mounted in the pod, but ImagePullSecrets are only accessed by the kubelet. More info: https://kubernetes.io/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod
        :param pulumi.Input[str] kind: Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        :param pulumi.Input['_meta.v1.ObjectMetaArgs'] metadata: Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
        :param pulumi.Input[Sequence[pulumi.Input['ObjectReferenceArgs']]] secrets: Secrets is the list of secrets allowed to be used by pods running using this ServiceAccount. More info: https://kubernetes.io/docs/concepts/configuration/secret
        """
        if api_version is not None:
            pulumi.set(__self__, "api_version", 'v1')
        if automount_service_account_token is not None:
            pulumi.set(__self__, "automount_service_account_token", automount_service_account_token)
        if image_pull_secrets is not None:
            pulumi.set(__self__, "image_pull_secrets", image_pull_secrets)
        if kind is not None:
            pulumi.set(__self__, "kind", 'ServiceAccount')
        if metadata is not None:
            pulumi.set(__self__, "metadata", metadata)
        if secrets is not None:
            pulumi.set(__self__, "secrets", secrets)

    @property
    @pulumi.getter(name="apiVersion")
    def api_version(self) -> Optional[pulumi.Input[str]]:
        """
        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        """
        return pulumi.get(self, "api_version")

    @api_version.setter
    def api_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "api_version", value)

    @property
    @pulumi.getter(name="automountServiceAccountToken")
    def automount_service_account_token(self) -> Optional[pulumi.Input[bool]]:
        """
        AutomountServiceAccountToken indicates whether pods running as this service account should have an API token automatically mounted. Can be overridden at the pod level.
        """
        return pulumi.get(self, "automount_service_account_token")

    @automount_service_account_token.setter
    def automount_service_account_token(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "automount_service_account_token", value)

    @property
    @pulumi.getter(name="imagePullSecrets")
    def image_pull_secrets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LocalObjectReferenceArgs']]]]:
        """
        ImagePullSecrets is a list of references to secrets in the same namespace to use for pulling any images in pods that reference this ServiceAccount. ImagePullSecrets are distinct from Secrets because Secrets can be mounted in the pod, but ImagePullSecrets are only accessed by the kubelet. More info: https://kubernetes.io/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod
        """
        return pulumi.get(self, "image_pull_secrets")

    @image_pull_secrets.setter
    def image_pull_secrets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LocalObjectReferenceArgs']]]]):
        pulumi.set(self, "image_pull_secrets", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def metadata(self) -> Optional[pulumi.Input['_meta.v1.ObjectMetaArgs']]:
        """
        Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
        """
        return pulumi.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: Optional[pulumi.Input['_meta.v1.ObjectMetaArgs']]):
        pulumi.set(self, "metadata", value)

    @property
    @pulumi.getter
    def secrets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ObjectReferenceArgs']]]]:
        """
        Secrets is the list of secrets allowed to be used by pods running using this ServiceAccount. More info: https://kubernetes.io/docs/concepts/configuration/secret
        """
        return pulumi.get(self, "secrets")

    @secrets.setter
    def secrets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ObjectReferenceArgs']]]]):
        pulumi.set(self, "secrets", value)


class ServiceAccount(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_version: Optional[pulumi.Input[str]] = None,
                 automount_service_account_token: Optional[pulumi.Input[bool]] = None,
                 image_pull_secrets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LocalObjectReferenceArgs']]]]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[pulumi.InputType['_meta.v1.ObjectMetaArgs']]] = None,
                 secrets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ObjectReferenceArgs']]]]] = None,
                 __props__=None):
        """
        ServiceAccount binds together: * a name, understood by users, and perhaps by peripheral systems, for an identity * a principal that can be authenticated and authorized * a set of secrets

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_version: APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        :param pulumi.Input[bool] automount_service_account_token: AutomountServiceAccountToken indicates whether pods running as this service account should have an API token automatically mounted. Can be overridden at the pod level.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LocalObjectReferenceArgs']]]] image_pull_secrets: ImagePullSecrets is a list of references to secrets in the same namespace to use for pulling any images in pods that reference this ServiceAccount. ImagePullSecrets are distinct from Secrets because Secrets can be mounted in the pod, but ImagePullSecrets are only accessed by the kubelet. More info: https://kubernetes.io/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod
        :param pulumi.Input[str] kind: Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        :param pulumi.Input[pulumi.InputType['_meta.v1.ObjectMetaArgs']] metadata: Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ObjectReferenceArgs']]]] secrets: Secrets is the list of secrets allowed to be used by pods running using this ServiceAccount. More info: https://kubernetes.io/docs/concepts/configuration/secret
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ServiceAccountArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ServiceAccount binds together: * a name, understood by users, and perhaps by peripheral systems, for an identity * a principal that can be authenticated and authorized * a set of secrets

        :param str resource_name: The name of the resource.
        :param ServiceAccountArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceAccountArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_version: Optional[pulumi.Input[str]] = None,
                 automount_service_account_token: Optional[pulumi.Input[bool]] = None,
                 image_pull_secrets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LocalObjectReferenceArgs']]]]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[pulumi.InputType['_meta.v1.ObjectMetaArgs']]] = None,
                 secrets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ObjectReferenceArgs']]]]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServiceAccountArgs.__new__(ServiceAccountArgs)

            __props__.__dict__["api_version"] = 'v1'
            __props__.__dict__["automount_service_account_token"] = automount_service_account_token
            __props__.__dict__["image_pull_secrets"] = image_pull_secrets
            __props__.__dict__["kind"] = 'ServiceAccount'
            __props__.__dict__["metadata"] = metadata
            __props__.__dict__["secrets"] = secrets
        super(ServiceAccount, __self__).__init__(
            'kubernetes:core/v1:ServiceAccount',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ServiceAccount':
        """
        Get an existing ServiceAccount resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ServiceAccountArgs.__new__(ServiceAccountArgs)

        __props__.__dict__["api_version"] = None
        __props__.__dict__["automount_service_account_token"] = None
        __props__.__dict__["image_pull_secrets"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["metadata"] = None
        __props__.__dict__["secrets"] = None
        return ServiceAccount(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiVersion")
    def api_version(self) -> pulumi.Output[Optional[str]]:
        """
        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        """
        return pulumi.get(self, "api_version")

    @property
    @pulumi.getter(name="automountServiceAccountToken")
    def automount_service_account_token(self) -> pulumi.Output[Optional[bool]]:
        """
        AutomountServiceAccountToken indicates whether pods running as this service account should have an API token automatically mounted. Can be overridden at the pod level.
        """
        return pulumi.get(self, "automount_service_account_token")

    @property
    @pulumi.getter(name="imagePullSecrets")
    def image_pull_secrets(self) -> pulumi.Output[Optional[Sequence['outputs.LocalObjectReference']]]:
        """
        ImagePullSecrets is a list of references to secrets in the same namespace to use for pulling any images in pods that reference this ServiceAccount. ImagePullSecrets are distinct from Secrets because Secrets can be mounted in the pod, but ImagePullSecrets are only accessed by the kubelet. More info: https://kubernetes.io/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod
        """
        return pulumi.get(self, "image_pull_secrets")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def metadata(self) -> pulumi.Output[Optional['_meta.v1.outputs.ObjectMeta']]:
        """
        Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def secrets(self) -> pulumi.Output[Optional[Sequence['outputs.ObjectReference']]]:
        """
        Secrets is the list of secrets allowed to be used by pods running using this ServiceAccount. More info: https://kubernetes.io/docs/concepts/configuration/secret
        """
        return pulumi.get(self, "secrets")

