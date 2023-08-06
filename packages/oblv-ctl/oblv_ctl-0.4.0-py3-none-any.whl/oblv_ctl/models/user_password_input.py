import json
from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="UserPasswordInput")


@attr.s(auto_attribs=True, repr=False)
class UserPasswordInput:
    """
    Attributes:
        old_password (str): Old password of user
        password (str): New password for user. It must contain a capital letter, a small letter, a digit, and a special
            character. Allowed special characters are - '#', '?', '!', '@', '$', '%', '^', '&', '*', '-'
    """

    old_password: str
    password: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        old_password = self.old_password
        password = self.password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "old_password": old_password,
                "password": password,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        old_password = d.pop("old_password")

        password = d.pop("password")

        user_password_input = cls(
            old_password=old_password,
            password=password,
        )

        user_password_input.additional_properties = d
        return user_password_input

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
