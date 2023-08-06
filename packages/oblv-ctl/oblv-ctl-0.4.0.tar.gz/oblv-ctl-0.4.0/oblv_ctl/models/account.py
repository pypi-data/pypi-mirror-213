import json
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Account")


@attr.s(auto_attribs=True, repr=False)
class Account:
    """
    Attributes:
        user_id (Union[Unset, str]):  Default: ''.
        user_login (Union[Unset, str]):  Default: ''.
        account_type (Union[Unset, str]):  Default: 'github'.
    """

    user_id: Union[Unset, str] = ""
    user_login: Union[Unset, str] = ""
    account_type: Union[Unset, str] = "github"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id
        user_login = self.user_login
        account_type = self.account_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if user_login is not UNSET:
            field_dict["user_login"] = user_login
        if account_type is not UNSET:
            field_dict["account_type"] = account_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_id = d.pop("user_id", UNSET)

        user_login = d.pop("user_login", UNSET)

        account_type = d.pop("account_type", UNSET)

        account = cls(
            user_id=user_id,
            user_login=user_login,
            account_type=account_type,
        )

        account.additional_properties = d
        return account

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
