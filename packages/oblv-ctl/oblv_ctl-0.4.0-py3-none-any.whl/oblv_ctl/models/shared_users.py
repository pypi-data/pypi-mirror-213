import json
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SharedUsers")


@attr.s(auto_attribs=True, repr=False)
class SharedUsers:
    """
    Attributes:
        role (List[str]):
        oblivious_user_id (Union[Unset, str]):  Default: ''.
        use_case (Union[Unset, str]):  Default: ''.
        oblivious_login (Union[Unset, str]):  Default: ''.
    """

    role: List[str]
    oblivious_user_id: Union[Unset, str] = ""
    use_case: Union[Unset, str] = ""
    oblivious_login: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        role = self.role

        oblivious_user_id = self.oblivious_user_id
        use_case = self.use_case
        oblivious_login = self.oblivious_login

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
            }
        )
        if oblivious_user_id is not UNSET:
            field_dict["oblivious_user_id"] = oblivious_user_id
        if use_case is not UNSET:
            field_dict["use_case"] = use_case
        if oblivious_login is not UNSET:
            field_dict["oblivious_login"] = oblivious_login

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        role = cast(List[str], d.pop("role"))

        oblivious_user_id = d.pop("oblivious_user_id", UNSET)

        use_case = d.pop("use_case", UNSET)

        oblivious_login = d.pop("oblivious_login", UNSET)

        shared_users = cls(
            role=role,
            oblivious_user_id=oblivious_user_id,
            use_case=use_case,
            oblivious_login=oblivious_login,
        )

        shared_users.additional_properties = d
        return shared_users

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
