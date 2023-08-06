import json
from typing import Any, Dict, List, Type, TypeVar, cast, Union

import attr
from .user_static_service_arguments import UserStaticServiceArguments
from .user_static_service_yaml_details import UserStaticServiceYamlDetails
from ..types import Unset, UNSET

T = TypeVar("T", bound="UserStaticService")


@attr.s(auto_attribs=True, repr=False)
class UserStaticService:
    """
    Attributes:
        id (str):
        name (str):
        description (str):
        repo_name (str):
        repo_owner (str):
        account_type (str):
        sha (str):
        arguments (UserStaticServiceArguments):
        pcr_codes (List[str]):
        min_infra_req (str):
        status (str):
        marketplace (bool):
        yaml_details (UserStaticServiceYamlDetails):
        service_full_name (Union[Unset, str]):  Default: ''.
    """

    id: str
    name: str
    description: str
    repo_name: str
    repo_owner: str
    account_type: str
    sha: str
    arguments: "UserStaticServiceArguments"
    pcr_codes: List[str]
    min_infra_req: str
    status: str
    marketplace: bool
    yaml_details: "UserStaticServiceYamlDetails"
    service_full_name: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        description = self.description
        repo_name = self.repo_name
        repo_owner = self.repo_owner
        account_type = self.account_type
        sha = self.sha
        arguments = self.arguments.to_dict()

        pcr_codes = self.pcr_codes

        min_infra_req = self.min_infra_req
        status = self.status
        marketplace = self.marketplace
        yaml_details = self.yaml_details.to_dict()

        service_full_name = self.service_full_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "repo_name": repo_name,
                "repo_owner": repo_owner,
                "account_type": account_type,
                "sha": sha,
                "arguments": arguments,
                "pcr_codes": pcr_codes,
                "min_infra_req": min_infra_req,
                "status": status,
                "marketplace": marketplace,
                "yaml_details": yaml_details,
            }
        )
        if service_full_name is not UNSET:
            field_dict["service_full_name"] = service_full_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        description = d.pop("description")

        repo_name = d.pop("repo_name")

        repo_owner = d.pop("repo_owner")

        account_type = d.pop("account_type")

        sha = d.pop("sha")

        arguments = UserStaticServiceArguments.from_dict(d.pop("arguments"))

        pcr_codes = cast(List[str], d.pop("pcr_codes"))

        min_infra_req = d.pop("min_infra_req")

        status = d.pop("status")

        marketplace = d.pop("marketplace")

        yaml_details = UserStaticServiceYamlDetails.from_dict(d.pop("yaml_details"))

        service_full_name = d.pop("service_full_name", UNSET)

        user_static_service = cls(
            id=id,
            name=name,
            description=description,
            repo_name=repo_name,
            repo_owner=repo_owner,
            account_type=account_type,
            sha=sha,
            arguments=arguments,
            pcr_codes=pcr_codes,
            min_infra_req=min_infra_req,
            status=status,
            marketplace=marketplace,
            yaml_details=yaml_details,
            service_full_name=service_full_name,
        )

        user_static_service.additional_properties = d
        return user_static_service

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
