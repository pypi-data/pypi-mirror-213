import json
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BuildArgsSchema")


@attr.s(auto_attribs=True, repr=False)
class BuildArgsSchema:
    """
    Attributes:
        sha (Union[Unset, str]):  Default: ''.
        arg_schema (Union[Unset, Any]):
    """

    sha: Union[Unset, str] = ""
    arg_schema: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        sha = self.sha
        arg_schema = self.arg_schema

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sha is not UNSET:
            field_dict["sha"] = sha
        if arg_schema is not UNSET:
            field_dict["arg_schema"] = arg_schema

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sha = d.pop("sha", UNSET)

        arg_schema = d.pop("arg_schema", UNSET)

        build_args_schema = cls(
            sha=sha,
            arg_schema=arg_schema,
        )

        build_args_schema.additional_properties = d
        return build_args_schema

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
