import json
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset
from .static_service_input_arguments import StaticServiceInputArguments

T = TypeVar("T", bound="StaticServiceInput")


@attr.s(auto_attribs=True, repr=False)
class StaticServiceInput:
    """
    Attributes:
        name (str): Service name. The name should start with an alphabet and can only contain numbers, alphabets, '_',
            '-'
        description (str): Service description
        repo_full_name (str): Repository full name in form - owner/repo from VCS.
        ref (str): The commit sha or the ref from which the service is to be created.
        arguments (Union[Unset, StaticServiceInputArguments, dict]): The arguments for docker build. From your service.yaml,
            the arguments added under "build_args".
    """

    name: str
    description: str
    repo_full_name: str
    ref: str
    arguments: Union[Unset, "StaticServiceInputArguments", dict] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        repo_full_name = self.repo_full_name
        ref = self.ref
        arguments: Union[Unset, Dict[str, Any]] = self.arguments
        if not isinstance(self.arguments, Unset) and not isinstance(self.arguments, dict):
            arguments = self.arguments.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "repo_full_name": repo_full_name,
                "ref": ref,
            }
        )
        if arguments is not UNSET:
            field_dict["arguments"] = arguments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        repo_full_name = d.pop("repo_full_name")

        ref = d.pop("ref")

        _arguments = d.pop("arguments", UNSET)
        arguments: Union[Unset, StaticServiceInputArguments, dict]
        if isinstance(_arguments, Unset):
            arguments = UNSET
        else:
            arguments = StaticServiceInputArguments.from_dict(_arguments)

        static_service_input = cls(
            name=name,
            description=description,
            repo_full_name=repo_full_name,
            ref=ref,
            arguments=arguments,
        )

        static_service_input.additional_properties = d
        return static_service_input

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
