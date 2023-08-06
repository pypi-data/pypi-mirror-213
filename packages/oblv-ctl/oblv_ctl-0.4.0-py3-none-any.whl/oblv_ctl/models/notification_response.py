import json
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NotificationResponse")


@attr.s(auto_attribs=True, repr=False)
class NotificationResponse:
    """
    Attributes:
        id (Union[Unset, str]):  Default: ''.
        summary (Union[Unset, str]):  Default: ''.
        type (Union[Unset, str]):  Default: ''.
        description (Union[Unset, str]):  Default: ''.
        created_at (Union[Unset, str]):  Default: ''.
        seen (Union[Unset, bool]):
    """

    id: Union[Unset, str] = ""
    summary: Union[Unset, str] = ""
    type: Union[Unset, str] = ""
    description: Union[Unset, str] = ""
    created_at: Union[Unset, str] = ""
    seen: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        summary = self.summary
        type = self.type
        description = self.description
        created_at = self.created_at
        seen = self.seen

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if summary is not UNSET:
            field_dict["summary"] = summary
        if type is not UNSET:
            field_dict["type"] = type
        if description is not UNSET:
            field_dict["description"] = description
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if seen is not UNSET:
            field_dict["seen"] = seen

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        summary = d.pop("summary", UNSET)

        type = d.pop("type", UNSET)

        description = d.pop("description", UNSET)

        created_at = d.pop("created_at", UNSET)

        seen = d.pop("seen", UNSET)

        notification_response = cls(
            id=id,
            summary=summary,
            type=type,
            description=description,
            created_at=created_at,
            seen=seen,
        )

        notification_response.additional_properties = d
        return notification_response

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
