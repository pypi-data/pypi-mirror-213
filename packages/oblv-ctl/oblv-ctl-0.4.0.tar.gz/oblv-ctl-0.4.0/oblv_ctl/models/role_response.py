import json
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RoleResponse")


@attr.s(auto_attribs=True, repr=False)
class RoleResponse:
    """
    Attributes:
        role_name (Union[Unset, str]):  Default: ''.
        role_description (Union[Unset, str]):  Default: ''.
    """

    role_name: Union[Unset, str] = ""
    role_description: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        role_name = self.role_name
        role_description = self.role_description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if role_name is not UNSET:
            field_dict["role_name"] = role_name
        if role_description is not UNSET:
            field_dict["role_description"] = role_description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        role_name = d.pop("role_name", UNSET)

        role_description = d.pop("role_description", UNSET)

        role_response = cls(
            role_name=role_name,
            role_description=role_description,
        )

        role_response.additional_properties = d
        return role_response

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
