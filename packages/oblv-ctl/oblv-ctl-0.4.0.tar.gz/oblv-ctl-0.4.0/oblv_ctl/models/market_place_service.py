import json
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="MarketPlaceService")


@attr.s(auto_attribs=True, repr=False)
class MarketPlaceService:
    """
    Attributes:
        id (Union[Unset, str]):  Default: ''.
        name (Union[Unset, str]):  Default: ''.
        description (Union[Unset, str]):  Default: ''.
        owner_name (Union[Unset, str]):  Default: ''.
        repo_full_name (Union[Unset, str]):  Default: ''.
        vcs_url (Union[Unset, str]):  Default: ''.
        pcr_codes (Union[Unset, List[str]]):
        min_infra_req (Union[Unset, str]):  Default: ''.
    """

    id: Union[Unset, str] = ""
    name: Union[Unset, str] = ""
    description: Union[Unset, str] = ""
    owner_name: Union[Unset, str] = ""
    repo_full_name: Union[Unset, str] = ""
    vcs_url: Union[Unset, str] = ""
    pcr_codes: Union[Unset, List[str]] = UNSET
    min_infra_req: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        description = self.description
        owner_name = self.owner_name
        repo_full_name = self.repo_full_name
        vcs_url = self.vcs_url
        pcr_codes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.pcr_codes, Unset):
            pcr_codes = self.pcr_codes

        min_infra_req = self.min_infra_req

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if owner_name is not UNSET:
            field_dict["owner_name"] = owner_name
        if repo_full_name is not UNSET:
            field_dict["repo_full_name"] = repo_full_name
        if vcs_url is not UNSET:
            field_dict["vcs_url"] = vcs_url
        if pcr_codes is not UNSET:
            field_dict["pcr_codes"] = pcr_codes
        if min_infra_req is not UNSET:
            field_dict["min_infra_req"] = min_infra_req

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        del d["owner"]
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        owner_name = d.pop("owner_name", UNSET)

        repo_full_name = d.pop("repo_full_name", UNSET)

        vcs_url = d.pop("vcs_url", UNSET)

        pcr_codes = cast(List[str], d.pop("pcr_codes", UNSET))

        min_infra_req = d.pop("min_infra_req", UNSET)

        market_place_service = cls(
            id=id,
            name=name,
            description=description,
            owner_name=owner_name,
            repo_full_name=repo_full_name,
            vcs_url=vcs_url,
            pcr_codes=pcr_codes,
            min_infra_req=min_infra_req,
        )

        market_place_service.additional_properties = d
        return market_place_service

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
