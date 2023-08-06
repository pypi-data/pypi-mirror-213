import json
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset
from .static_service_arguments import StaticServiceArguments

T = TypeVar("T", bound="StaticService")


@attr.s(auto_attribs=True, repr=False)
class StaticService:
    """
    Attributes:
        id (Union[Unset, str]):  Default: ''.
        name (Union[Unset, str]):  Default: ''.
        description (Union[Unset, str]):  Default: ''.
        sha (Union[Unset, str]):  Default: ''.
        arguments (Union[Unset, StaticServiceArguments]):
        pcr_codes (Union[Unset, List[str]]):
        min_infra_req (Union[Unset, str]):  Default: ''.
        status (Union[Unset, str]):  Default: ''.
        marketplace (Union[Unset, bool]):
        repo_full_name (Union[Unset, str]):  Default: ''.
    """

    id: Union[Unset, str] = ""
    name: Union[Unset, str] = ""
    description: Union[Unset, str] = ""
    sha: Union[Unset, str] = ""
    arguments: Union[Unset, "StaticServiceArguments"] = UNSET
    pcr_codes: Union[Unset, List[str]] = UNSET
    min_infra_req: Union[Unset, str] = ""
    status: Union[Unset, str] = ""
    marketplace: Union[Unset, bool] = False
    repo_full_name: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        description = self.description
        sha = self.sha
        arguments: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.arguments, Unset):
            arguments = self.arguments.to_dict()

        pcr_codes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.pcr_codes, Unset):
            pcr_codes = self.pcr_codes

        min_infra_req = self.min_infra_req
        status = self.status
        marketplace = self.marketplace
        repo_full_name = self.repo_full_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if sha is not UNSET:
            field_dict["sha"] = sha
        if arguments is not UNSET:
            field_dict["arguments"] = arguments
        if pcr_codes is not UNSET:
            field_dict["pcr_codes"] = pcr_codes
        if min_infra_req is not UNSET:
            field_dict["min_infra_req"] = min_infra_req
        if status is not UNSET:
            field_dict["status"] = status
        if marketplace is not UNSET:
            field_dict["marketplace"] = marketplace
        if repo_full_name is not UNSET:
            field_dict["repo_full_name"] = repo_full_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        sha = d.pop("sha", UNSET)

        _arguments = d.pop("arguments", UNSET)
        arguments: Union[Unset, StaticServiceArguments]
        if isinstance(_arguments, Unset):
            arguments = UNSET
        else:
            arguments = StaticServiceArguments.from_dict(_arguments)

        pcr_codes = cast(List[str], d.pop("pcr_codes", UNSET))

        min_infra_req = d.pop("min_infra_req", UNSET)

        status = d.pop("status", UNSET)

        marketplace = d.pop("marketplace", UNSET)

        repo_full_name = d.pop("repo_full_name", UNSET)

        static_service = cls(
            id=id,
            name=name,
            description=description,
            sha=sha,
            arguments=arguments,
            pcr_codes=pcr_codes,
            min_infra_req=min_infra_req,
            status=status,
            marketplace=marketplace,
            repo_full_name=repo_full_name,
        )

        static_service.additional_properties = d
        return static_service

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
