import json
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RepoAllResponse")


@attr.s(auto_attribs=True, repr=False)
class RepoAllResponse:
    """
    Attributes:
        name (Union[Unset, str]):  Default: ''.
        owner_login (Union[Unset, str]):  Default: ''.
        account_type (Union[Unset, str]):  Default: ''.
    """

    name: Union[Unset, str] = ""
    owner_login: Union[Unset, str] = ""
    account_type: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        owner_login = self.owner_login
        account_type = self.account_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if owner_login is not UNSET:
            field_dict["owner_login"] = owner_login
        if account_type is not UNSET:
            field_dict["account_type"] = account_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        owner_login = d.pop("owner_login", UNSET)

        account_type = d.pop("account_type", UNSET)

        repo_all_response = cls(
            name=name,
            owner_login=owner_login,
            account_type=account_type,
        )

        repo_all_response.additional_properties = d
        return repo_all_response

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
