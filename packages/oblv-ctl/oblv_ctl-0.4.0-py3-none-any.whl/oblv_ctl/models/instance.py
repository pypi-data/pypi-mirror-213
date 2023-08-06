import json
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Instance")


@attr.s(auto_attribs=True, repr=False)
class Instance:
    """
    Attributes:
        region_name (Union[Unset, str]):  Default: ''.
        stack_name (Union[Unset, str]):  Default: ''.
        instance_type (Union[Unset, str]):  Default: ''.
        instance_url (Union[Unset, str]):  Default: ''.
        service_url (Union[Unset, str]):  Default: ''.
        build_log_location (Union[Unset, str]):  Default: ''.
    """

    region_name: Union[Unset, str] = ""
    stack_name: Union[Unset, str] = ""
    instance_type: Union[Unset, str] = ""
    instance_url: Union[Unset, str] = ""
    service_url: Union[Unset, str] = ""
    build_log_location: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        region_name = self.region_name
        stack_name = self.stack_name
        instance_type = self.instance_type
        instance_url = self.instance_url
        service_url = self.service_url
        build_log_location = self.build_log_location

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if region_name is not UNSET:
            field_dict["region_name"] = region_name
        if stack_name is not UNSET:
            field_dict["stack_name"] = stack_name
        if instance_type is not UNSET:
            field_dict["instance_type"] = instance_type
        if instance_url is not UNSET:
            field_dict["instance_url"] = instance_url
        if service_url is not UNSET:
            field_dict["service_url"] = service_url
        if build_log_location is not UNSET:
            field_dict["build_log_location"] = build_log_location

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        region_name = d.pop("region_name", UNSET)

        stack_name = d.pop("stack_name", UNSET)

        instance_type = d.pop("instance_type", UNSET)

        instance_url = d.pop("instance_url", UNSET)

        service_url = d.pop("service_url", UNSET)

        build_log_location = d.pop("build_log_location", UNSET)

        instance = cls(
            region_name=region_name,
            stack_name=stack_name,
            instance_type=instance_type,
            instance_url=instance_url,
            service_url=service_url,
            build_log_location=build_log_location,
        )

        instance.additional_properties = d
        return instance

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def __str__(self):
        return json.dumps(self.to_dict(), indent=2)

    def __repr__(self):
        return str(self)
