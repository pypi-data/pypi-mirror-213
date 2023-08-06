import json
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateDeploymentInput")


@attr.s(auto_attribs=True, repr=False)
class CreateDeploymentInput:
    """
    Attributes:
        owner (str): Repository Owner
        repo (str): Repository Name
        account_type (str): VCS Account (Only 'github' supported as of now)
        ref (str): Service ref
        ref_type (str): Service ref type
        region_name (str): AWS supported region the deployment must be deployed in.
        deployment_name (str): Deployment Name
        is_dev_env (bool): Deployment Environment
        tags (List[str]): Deployment Tags
        build_args (Any): Deployment build args
        visibility (Union[Unset, str]): Deployment Visibility Default: 'private'.
    """

    owner: str
    repo: str
    account_type: str
    ref: str
    ref_type: str
    region_name: str
    deployment_name: str
    is_dev_env: bool
    tags: List[str]
    build_args: Any
    visibility: Union[Unset, str] = "private"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        owner = self.owner
        repo = self.repo
        account_type = self.account_type
        ref = self.ref
        ref_type = self.ref_type
        region_name = self.region_name
        deployment_name = self.deployment_name
        is_dev_env = self.is_dev_env
        tags = self.tags

        build_args = self.build_args
        visibility = self.visibility

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "owner": owner,
                "repo": repo,
                "account_type": account_type,
                "ref": ref,
                "ref_type": ref_type,
                "region_name": region_name,
                "deployment_name": deployment_name,
                "is_dev_env": is_dev_env,
                "tags": tags,
                "build_args": build_args,
            }
        )
        if visibility is not UNSET:
            field_dict["visibility"] = visibility

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        owner = d.pop("owner")

        repo = d.pop("repo")

        account_type = d.pop("account_type")

        ref = d.pop("ref")

        ref_type = d.pop("ref_type")

        region_name = d.pop("region_name")

        deployment_name = d.pop("deployment_name")

        is_dev_env = d.pop("is_dev_env")

        tags = cast(List[str], d.pop("tags"))

        build_args = d.pop("build_args")

        visibility = d.pop("visibility", UNSET)

        create_deployment_input = cls(
            owner=owner,
            repo=repo,
            account_type=account_type,
            ref=ref,
            ref_type=ref_type,
            region_name=region_name,
            deployment_name=deployment_name,
            is_dev_env=is_dev_env,
            tags=tags,
            build_args=build_args,
            visibility=visibility,
        )

        create_deployment_input.additional_properties = d
        return create_deployment_input

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