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

__all__ = ['ClusterRoleBindingArgs', 'ClusterRoleBinding']

@pulumi.input_type
class ClusterRoleBindingArgs:
    def __init__(__self__, *,
                 role_ref: pulumi.Input['RoleRefArgs'],
                 api_version: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input['_meta.v1.ObjectMetaArgs']] = None,
                 subjects: Optional[pulumi.Input[Sequence[pulumi.Input['SubjectArgs']]]] = None):
        """
        The set of arguments for constructing a ClusterRoleBinding resource.
        :param pulumi.Input['RoleRefArgs'] role_ref: RoleRef can only reference a ClusterRole in the global namespace. If the RoleRef cannot be resolved, the Authorizer must return an error.
        :param pulumi.Input[str] api_version: APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        :param pulumi.Input[str] kind: Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        :param pulumi.Input['_meta.v1.ObjectMetaArgs'] metadata: Standard object's metadata.
        :param pulumi.Input[Sequence[pulumi.Input['SubjectArgs']]] subjects: Subjects holds references to the objects the role applies to.
        """
        pulumi.set(__self__, "role_ref", role_ref)
        if api_version is not None:
            pulumi.set(__self__, "api_version", 'rbac.authorization.k8s.io/v1beta1')
        if kind is not None:
            pulumi.set(__self__, "kind", 'ClusterRoleBinding')
        if metadata is not None:
            pulumi.set(__self__, "metadata", metadata)
        if subjects is not None:
            pulumi.set(__self__, "subjects", subjects)

    @property
    @pulumi.getter(name="roleRef")
    def role_ref(self) -> pulumi.Input['RoleRefArgs']:
        """
        RoleRef can only reference a ClusterRole in the global namespace. If the RoleRef cannot be resolved, the Authorizer must return an error.
        """
        return pulumi.get(self, "role_ref")

    @role_ref.setter
    def role_ref(self, value: pulumi.Input['RoleRefArgs']):
        pulumi.set(self, "role_ref", value)

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
        """
        Standard object's metadata.
        """
        return pulumi.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: Optional[pulumi.Input['_meta.v1.ObjectMetaArgs']]):
        pulumi.set(self, "metadata", value)

    @property
    @pulumi.getter
    def subjects(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SubjectArgs']]]]:
        """
        Subjects holds references to the objects the role applies to.
        """
        return pulumi.get(self, "subjects")

    @subjects.setter
    def subjects(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SubjectArgs']]]]):
        pulumi.set(self, "subjects", value)


class ClusterRoleBinding(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_version: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[pulumi.InputType['_meta.v1.ObjectMetaArgs']]] = None,
                 role_ref: Optional[pulumi.Input[pulumi.InputType['RoleRefArgs']]] = None,
                 subjects: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SubjectArgs']]]]] = None,
                 __props__=None):
        """
        ClusterRoleBinding references a ClusterRole, but not contain it.  It can reference a ClusterRole in the global namespace, and adds who information via Subject. Deprecated in v1.17 in favor of rbac.authorization.k8s.io/v1 ClusterRoleBinding, and will no longer be served in v1.22.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_version: APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        :param pulumi.Input[str] kind: Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        :param pulumi.Input[pulumi.InputType['_meta.v1.ObjectMetaArgs']] metadata: Standard object's metadata.
        :param pulumi.Input[pulumi.InputType['RoleRefArgs']] role_ref: RoleRef can only reference a ClusterRole in the global namespace. If the RoleRef cannot be resolved, the Authorizer must return an error.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SubjectArgs']]]] subjects: Subjects holds references to the objects the role applies to.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ClusterRoleBindingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ClusterRoleBinding references a ClusterRole, but not contain it.  It can reference a ClusterRole in the global namespace, and adds who information via Subject. Deprecated in v1.17 in favor of rbac.authorization.k8s.io/v1 ClusterRoleBinding, and will no longer be served in v1.22.

        :param str resource_name: The name of the resource.
        :param ClusterRoleBindingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ClusterRoleBindingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_version: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[pulumi.InputType['_meta.v1.ObjectMetaArgs']]] = None,
                 role_ref: Optional[pulumi.Input[pulumi.InputType['RoleRefArgs']]] = None,
                 subjects: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SubjectArgs']]]]] = None,
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
            __props__ = ClusterRoleBindingArgs.__new__(ClusterRoleBindingArgs)

            __props__.__dict__["api_version"] = 'rbac.authorization.k8s.io/v1beta1'
            __props__.__dict__["kind"] = 'ClusterRoleBinding'
            __props__.__dict__["metadata"] = metadata
            if role_ref is None and not opts.urn:
                raise TypeError("Missing required property 'role_ref'")
            __props__.__dict__["role_ref"] = role_ref
            __props__.__dict__["subjects"] = subjects
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="kubernetes:rbac.authorization.k8s.io/v1:ClusterRoleBinding"), pulumi.Alias(type_="kubernetes:rbac.authorization.k8s.io/v1alpha1:ClusterRoleBinding")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ClusterRoleBinding, __self__).__init__(
            'kubernetes:rbac.authorization.k8s.io/v1beta1:ClusterRoleBinding',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ClusterRoleBinding':
        """
        Get an existing ClusterRoleBinding resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ClusterRoleBindingArgs.__new__(ClusterRoleBindingArgs)

        __props__.__dict__["api_version"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["metadata"] = None
        __props__.__dict__["role_ref"] = None
        __props__.__dict__["subjects"] = None
        return ClusterRoleBinding(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiVersion")
    def api_version(self) -> pulumi.Output[Optional[str]]:
        """
        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        """
        return pulumi.get(self, "api_version")

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
        Standard object's metadata.
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter(name="roleRef")
    def role_ref(self) -> pulumi.Output['outputs.RoleRef']:
        """
        RoleRef can only reference a ClusterRole in the global namespace. If the RoleRef cannot be resolved, the Authorizer must return an error.
        """
        return pulumi.get(self, "role_ref")

    @property
    @pulumi.getter
    def subjects(self) -> pulumi.Output[Optional[Sequence['outputs.Subject']]]:
        """
        Subjects holds references to the objects the role applies to.
        """
        return pulumi.get(self, "subjects")

