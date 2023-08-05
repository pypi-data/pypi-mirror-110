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

__all__ = [
    'APIService',
    'APIServiceCondition',
    'APIServiceSpec',
    'APIServiceStatus',
    'ServiceReference',
]

@pulumi.output_type
class APIService(dict):
    """
    APIService represents a server for a particular GroupVersion. Name must be "version.group".
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "apiVersion":
            suggest = "api_version"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in APIService. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        APIService.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        APIService.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 api_version: Optional[str] = None,
                 kind: Optional[str] = None,
                 metadata: Optional['_meta.v1.outputs.ObjectMeta'] = None,
                 spec: Optional['outputs.APIServiceSpec'] = None,
                 status: Optional['outputs.APIServiceStatus'] = None):
        """
        APIService represents a server for a particular GroupVersion. Name must be "version.group".
        :param str api_version: APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        :param str kind: Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        :param 'APIServiceSpecArgs' spec: Spec contains information for locating and communicating with a server
        :param 'APIServiceStatusArgs' status: Status contains derived information about an API server
        """
        if api_version is not None:
            pulumi.set(__self__, "api_version", 'apiregistration.k8s.io/v1')
        if kind is not None:
            pulumi.set(__self__, "kind", 'APIService')
        if metadata is not None:
            pulumi.set(__self__, "metadata", metadata)
        if spec is not None:
            pulumi.set(__self__, "spec", spec)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="apiVersion")
    def api_version(self) -> Optional[str]:
        """
        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        """
        return pulumi.get(self, "api_version")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def metadata(self) -> Optional['_meta.v1.outputs.ObjectMeta']:
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def spec(self) -> Optional['outputs.APIServiceSpec']:
        """
        Spec contains information for locating and communicating with a server
        """
        return pulumi.get(self, "spec")

    @property
    @pulumi.getter
    def status(self) -> Optional['outputs.APIServiceStatus']:
        """
        Status contains derived information about an API server
        """
        return pulumi.get(self, "status")


@pulumi.output_type
class APIServiceCondition(dict):
    """
    APIServiceCondition describes the state of an APIService at a particular point
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "lastTransitionTime":
            suggest = "last_transition_time"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in APIServiceCondition. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        APIServiceCondition.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        APIServiceCondition.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 status: str,
                 type: str,
                 last_transition_time: Optional[str] = None,
                 message: Optional[str] = None,
                 reason: Optional[str] = None):
        """
        APIServiceCondition describes the state of an APIService at a particular point
        :param str status: Status is the status of the condition. Can be True, False, Unknown.
        :param str type: Type is the type of the condition.
        :param str last_transition_time: Last time the condition transitioned from one status to another.
        :param str message: Human-readable message indicating details about last transition.
        :param str reason: Unique, one-word, CamelCase reason for the condition's last transition.
        """
        pulumi.set(__self__, "status", status)
        pulumi.set(__self__, "type", type)
        if last_transition_time is not None:
            pulumi.set(__self__, "last_transition_time", last_transition_time)
        if message is not None:
            pulumi.set(__self__, "message", message)
        if reason is not None:
            pulumi.set(__self__, "reason", reason)

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status is the status of the condition. Can be True, False, Unknown.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type is the type of the condition.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="lastTransitionTime")
    def last_transition_time(self) -> Optional[str]:
        """
        Last time the condition transitioned from one status to another.
        """
        return pulumi.get(self, "last_transition_time")

    @property
    @pulumi.getter
    def message(self) -> Optional[str]:
        """
        Human-readable message indicating details about last transition.
        """
        return pulumi.get(self, "message")

    @property
    @pulumi.getter
    def reason(self) -> Optional[str]:
        """
        Unique, one-word, CamelCase reason for the condition's last transition.
        """
        return pulumi.get(self, "reason")


@pulumi.output_type
class APIServiceSpec(dict):
    """
    APIServiceSpec contains information for locating and communicating with a server. Only https is supported, though you are able to disable certificate verification.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "groupPriorityMinimum":
            suggest = "group_priority_minimum"
        elif key == "versionPriority":
            suggest = "version_priority"
        elif key == "caBundle":
            suggest = "ca_bundle"
        elif key == "insecureSkipTLSVerify":
            suggest = "insecure_skip_tls_verify"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in APIServiceSpec. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        APIServiceSpec.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        APIServiceSpec.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 group_priority_minimum: int,
                 version_priority: int,
                 ca_bundle: Optional[str] = None,
                 group: Optional[str] = None,
                 insecure_skip_tls_verify: Optional[bool] = None,
                 service: Optional['outputs.ServiceReference'] = None,
                 version: Optional[str] = None):
        """
        APIServiceSpec contains information for locating and communicating with a server. Only https is supported, though you are able to disable certificate verification.
        :param int group_priority_minimum: GroupPriorityMininum is the priority this group should have at least. Higher priority means that the group is preferred by clients over lower priority ones. Note that other versions of this group might specify even higher GroupPriorityMininum values such that the whole group gets a higher priority. The primary sort is based on GroupPriorityMinimum, ordered highest number to lowest (20 before 10). The secondary sort is based on the alphabetical comparison of the name of the object.  (v1.bar before v1.foo) We'd recommend something like: *.k8s.io (except extensions) at 18000 and PaaSes (OpenShift, Deis) are recommended to be in the 2000s
        :param int version_priority: VersionPriority controls the ordering of this API version inside of its group.  Must be greater than zero. The primary sort is based on VersionPriority, ordered highest to lowest (20 before 10). Since it's inside of a group, the number can be small, probably in the 10s. In case of equal version priorities, the version string will be used to compute the order inside a group. If the version string is "kube-like", it will sort above non "kube-like" version strings, which are ordered lexicographically. "Kube-like" versions start with a "v", then are followed by a number (the major version), then optionally the string "alpha" or "beta" and another number (the minor version). These are sorted first by GA > beta > alpha (where GA is a version with no suffix such as beta or alpha), and then by comparing major version, then minor version. An example sorted list of versions: v10, v2, v1, v11beta2, v10beta3, v3beta1, v12alpha1, v11alpha2, foo1, foo10.
        :param str ca_bundle: CABundle is a PEM encoded CA bundle which will be used to validate an API server's serving certificate. If unspecified, system trust roots on the apiserver are used.
        :param str group: Group is the API group name this server hosts
        :param bool insecure_skip_tls_verify: InsecureSkipTLSVerify disables TLS certificate verification when communicating with this server. This is strongly discouraged.  You should use the CABundle instead.
        :param 'ServiceReferenceArgs' service: Service is a reference to the service for this API server.  It must communicate on port 443. If the Service is nil, that means the handling for the API groupversion is handled locally on this server. The call will simply delegate to the normal handler chain to be fulfilled.
        :param str version: Version is the API version this server hosts.  For example, "v1"
        """
        pulumi.set(__self__, "group_priority_minimum", group_priority_minimum)
        pulumi.set(__self__, "version_priority", version_priority)
        if ca_bundle is not None:
            pulumi.set(__self__, "ca_bundle", ca_bundle)
        if group is not None:
            pulumi.set(__self__, "group", group)
        if insecure_skip_tls_verify is not None:
            pulumi.set(__self__, "insecure_skip_tls_verify", insecure_skip_tls_verify)
        if service is not None:
            pulumi.set(__self__, "service", service)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="groupPriorityMinimum")
    def group_priority_minimum(self) -> int:
        """
        GroupPriorityMininum is the priority this group should have at least. Higher priority means that the group is preferred by clients over lower priority ones. Note that other versions of this group might specify even higher GroupPriorityMininum values such that the whole group gets a higher priority. The primary sort is based on GroupPriorityMinimum, ordered highest number to lowest (20 before 10). The secondary sort is based on the alphabetical comparison of the name of the object.  (v1.bar before v1.foo) We'd recommend something like: *.k8s.io (except extensions) at 18000 and PaaSes (OpenShift, Deis) are recommended to be in the 2000s
        """
        return pulumi.get(self, "group_priority_minimum")

    @property
    @pulumi.getter(name="versionPriority")
    def version_priority(self) -> int:
        """
        VersionPriority controls the ordering of this API version inside of its group.  Must be greater than zero. The primary sort is based on VersionPriority, ordered highest to lowest (20 before 10). Since it's inside of a group, the number can be small, probably in the 10s. In case of equal version priorities, the version string will be used to compute the order inside a group. If the version string is "kube-like", it will sort above non "kube-like" version strings, which are ordered lexicographically. "Kube-like" versions start with a "v", then are followed by a number (the major version), then optionally the string "alpha" or "beta" and another number (the minor version). These are sorted first by GA > beta > alpha (where GA is a version with no suffix such as beta or alpha), and then by comparing major version, then minor version. An example sorted list of versions: v10, v2, v1, v11beta2, v10beta3, v3beta1, v12alpha1, v11alpha2, foo1, foo10.
        """
        return pulumi.get(self, "version_priority")

    @property
    @pulumi.getter(name="caBundle")
    def ca_bundle(self) -> Optional[str]:
        """
        CABundle is a PEM encoded CA bundle which will be used to validate an API server's serving certificate. If unspecified, system trust roots on the apiserver are used.
        """
        return pulumi.get(self, "ca_bundle")

    @property
    @pulumi.getter
    def group(self) -> Optional[str]:
        """
        Group is the API group name this server hosts
        """
        return pulumi.get(self, "group")

    @property
    @pulumi.getter(name="insecureSkipTLSVerify")
    def insecure_skip_tls_verify(self) -> Optional[bool]:
        """
        InsecureSkipTLSVerify disables TLS certificate verification when communicating with this server. This is strongly discouraged.  You should use the CABundle instead.
        """
        return pulumi.get(self, "insecure_skip_tls_verify")

    @property
    @pulumi.getter
    def service(self) -> Optional['outputs.ServiceReference']:
        """
        Service is a reference to the service for this API server.  It must communicate on port 443. If the Service is nil, that means the handling for the API groupversion is handled locally on this server. The call will simply delegate to the normal handler chain to be fulfilled.
        """
        return pulumi.get(self, "service")

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Version is the API version this server hosts.  For example, "v1"
        """
        return pulumi.get(self, "version")


@pulumi.output_type
class APIServiceStatus(dict):
    """
    APIServiceStatus contains derived information about an API server
    """
    def __init__(__self__, *,
                 conditions: Optional[Sequence['outputs.APIServiceCondition']] = None):
        """
        APIServiceStatus contains derived information about an API server
        :param Sequence['APIServiceConditionArgs'] conditions: Current service state of apiService.
        """
        if conditions is not None:
            pulumi.set(__self__, "conditions", conditions)

    @property
    @pulumi.getter
    def conditions(self) -> Optional[Sequence['outputs.APIServiceCondition']]:
        """
        Current service state of apiService.
        """
        return pulumi.get(self, "conditions")


@pulumi.output_type
class ServiceReference(dict):
    """
    ServiceReference holds a reference to Service.legacy.k8s.io
    """
    def __init__(__self__, *,
                 name: Optional[str] = None,
                 namespace: Optional[str] = None,
                 port: Optional[int] = None):
        """
        ServiceReference holds a reference to Service.legacy.k8s.io
        :param str name: Name is the name of the service
        :param str namespace: Namespace is the namespace of the service
        :param int port: If specified, the port on the service that hosting webhook. Default to 443 for backward compatibility. `port` should be a valid port number (1-65535, inclusive).
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if port is not None:
            pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name is the name of the service
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def namespace(self) -> Optional[str]:
        """
        Namespace is the namespace of the service
        """
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter
    def port(self) -> Optional[int]:
        """
        If specified, the port on the service that hosting webhook. Default to 443 for backward compatibility. `port` should be a valid port number (1-65535, inclusive).
        """
        return pulumi.get(self, "port")


