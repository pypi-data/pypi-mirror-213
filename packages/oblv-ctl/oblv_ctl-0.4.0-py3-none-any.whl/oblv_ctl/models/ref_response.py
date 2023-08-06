import json
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RefResponse")


@attr.s(auto_attribs=True, repr=False)
class RefResponse:
    """
    Attributes:
        tags (Union[Unset, List[str]]):
        branch (Union[Unset, List[str]]):
    """

    tags: Union[Unset, List[str]] = UNSET
    branch: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        branch: Union[Unset, List[str]] = UNSET
        if not isinstance(self.branch, Unset):
            branch = self.branch

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tags is not UNSET:
            field_dict["tags"] = tags
        if branch is not UNSET:
            field_dict["branch"] = branch

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tags = cast(List[str], d.pop("tags", UNSET))

        branch = cast(List[str], d.pop("branch", UNSET))

        ref_response = cls(
            tags=tags,
            branch=branch,
        )

        ref_response.additional_properties = d
        return ref_response

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
