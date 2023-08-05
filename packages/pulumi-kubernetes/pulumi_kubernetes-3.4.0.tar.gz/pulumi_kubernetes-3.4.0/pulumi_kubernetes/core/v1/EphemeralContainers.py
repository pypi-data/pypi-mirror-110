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

__all__ = ['EphemeralContainersArgs', 'EphemeralContainers']

@pulumi.input_type
class EphemeralContainersArgs:
    def __init__(__self__, *,
                 ephemeral_containers: pulumi.Input[Sequence[pulumi.Input['EphemeralContainerArgs']]],
                 api_version: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input['_meta.v1.ObjectMetaArgs']] = None):
        """
        The set of arguments for constructing a EphemeralContainers resource.
        :param pulumi.Input[Sequence[pulumi.Input['EphemeralContainerArgs']]] ephemeral_containers: A list of ephemeral containers associated with this pod. New ephemeral containers may be appended to this list, but existing ephemeral containers may not be removed or modified.
        :param pulumi.Input[str] api_version: APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        :param pulumi.Input[str] kind: Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        """
        pulumi.set(__self__, "ephemeral_containers", ephemeral_containers)
        if api_version is not None:
            pulumi.set(__self__, "api_version", 'v1')
        if kind is not None:
            pulumi.set(__self__, "kind", 'EphemeralContainers')
        if metadata is not None:
            pulumi.set(__self__, "metadata", metadata)

    @property
    @pulumi.getter(name="ephemeralContainers")
    def ephemeral_containers(self) -> pulumi.Input[Sequence[pulumi.Input['EphemeralContainerArgs']]]:
        """
        A list of ephemeral containers associated with this pod. New ephemeral containers may be appended to this list, but existing ephemeral containers may not be removed or modified.
        """
        return pulumi.get(self, "ephemeral_containers")

    @ephemeral_containers.setter
    def ephemeral_containers(self, value: pulumi.Input[Sequence[pulumi.Input['EphemeralContainerArgs']]]):
        pulumi.set(self, "ephemeral_containers", value)

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
        return pulumi.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: Optional[pulumi.Input['_meta.v1.ObjectMetaArgs']]):
        pulumi.set(self, "metadata", value)


class EphemeralContainers(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_version: Optional[pulumi.Input[str]] = None,
                 ephemeral_containers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EphemeralContainerArgs']]]]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[pulumi.InputType['_meta.v1.ObjectMetaArgs']]] = None,
                 __props__=None):
        """
        A list of ephemeral containers used with the Pod ephemeralcontainers subresource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_version: APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EphemeralContainerArgs']]]] ephemeral_containers: A list of ephemeral containers associated with this pod. New ephemeral containers may be appended to this list, but existing ephemeral containers may not be removed or modified.
        :param pulumi.Input[str] kind: Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EphemeralContainersArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A list of ephemeral containers used with the Pod ephemeralcontainers subresource.

        :param str resource_name: The name of the resource.
        :param EphemeralContainersArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EphemeralContainersArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_version: Optional[pulumi.Input[str]] = None,
                 ephemeral_containers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EphemeralContainerArgs']]]]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[pulumi.InputType['_meta.v1.ObjectMetaArgs']]] = None,
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
            __props__ = EphemeralContainersArgs.__new__(EphemeralContainersArgs)

            __props__.__dict__["api_version"] = 'v1'
            if ephemeral_containers is None and not opts.urn:
                raise TypeError("Missing required property 'ephemeral_containers'")
            __props__.__dict__["ephemeral_containers"] = ephemeral_containers
            __props__.__dict__["kind"] = 'EphemeralContainers'
            __props__.__dict__["metadata"] = metadata
        super(EphemeralContainers, __self__).__init__(
            'kubernetes:core/v1:EphemeralContainers',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'EphemeralContainers':
        """
        Get an existing EphemeralContainers resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = EphemeralContainersArgs.__new__(EphemeralContainersArgs)

        __props__.__dict__["api_version"] = None
        __props__.__dict__["ephemeral_containers"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["metadata"] = None
        return EphemeralContainers(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiVersion")
    def api_version(self) -> pulumi.Output[Optional[str]]:
        """
        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        """
        return pulumi.get(self, "api_version")

    @property
    @pulumi.getter(name="ephemeralContainers")
    def ephemeral_containers(self) -> pulumi.Output[Sequence['outputs.EphemeralContainer']]:
        """
        A list of ephemeral containers associated with this pod. New ephemeral containers may be appended to this list, but existing ephemeral containers may not be removed or modified.
        """
        return pulumi.get(self, "ephemeral_containers")

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
        return pulumi.get(self, "metadata")

