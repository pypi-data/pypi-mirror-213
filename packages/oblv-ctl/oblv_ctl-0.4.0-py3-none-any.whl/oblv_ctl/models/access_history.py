import json
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccessHistory")


@attr.s(auto_attribs=True, repr=False)
class AccessHistory:
    """
    Attributes:
        action (Union[Unset, str]):  Default: ''.
        timestamp (Union[Unset, str]):  Default: '21-05-2023 07:37:30'.
        oblivious_user_id (Union[Unset, str]):  Default: ''.
        role (Union[Unset, str]):
    """

    action: Union[Unset, str] = ""
    timestamp: Union[Unset, str] = "21-05-2023 07:37:30"
    oblivious_user_id: Union[Unset, str] = ""
    role: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        action = self.action
        timestamp = self.timestamp
        oblivious_user_id = self.oblivious_user_id
        role = self.role

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if action is not UNSET:
            field_dict["action"] = action
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if oblivious_user_id is not UNSET:
            field_dict["oblivious_user_id"] = oblivious_user_id
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        action = d.pop("action", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        oblivious_user_id = d.pop("oblivious_user_id", UNSET)

        role = d.pop("role", UNSET)

        access_history = cls(
            action=action,
            timestamp=timestamp,
            oblivious_user_id=oblivious_user_id,
            role=role,
        )

        access_history.additional_properties = d
        return access_history

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
