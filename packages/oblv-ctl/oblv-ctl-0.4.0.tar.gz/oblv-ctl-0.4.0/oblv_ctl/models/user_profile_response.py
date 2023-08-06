import json
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserProfileResponse")


@attr.s(auto_attribs=True, repr=False)
class UserProfileResponse:
    """
    Attributes:
        oblivious_login (Union[Unset, str]):  Default: ''.
        email (Union[Unset, str]):  Default: ''.
        user_name (Union[Unset, str]):  Default: ''.
        public_key (Union[Unset, str]):  Default: ''.
    """

    oblivious_login: Union[Unset, str] = ""
    email: Union[Unset, str] = ""
    user_name: Union[Unset, str] = ""
    public_key: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        oblivious_login = self.oblivious_login
        email = self.email
        user_name = self.user_name
        public_key = self.public_key

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if oblivious_login is not UNSET:
            field_dict["oblivious_login"] = oblivious_login
        if email is not UNSET:
            field_dict["email"] = email
        if user_name is not UNSET:
            field_dict["user_name"] = user_name
        if public_key is not UNSET:
            field_dict["public_key"] = public_key

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        oblivious_login = d.pop("oblivious_login", UNSET)

        email = d.pop("email", UNSET)

        user_name = d.pop("user_name", UNSET)

        public_key = d.pop("public_key", UNSET)

        user_profile_response = cls(
            oblivious_login=oblivious_login,
            email=email,
            user_name=user_name,
            public_key=public_key,
        )

        user_profile_response.additional_properties = d
        return user_profile_response

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
