import json
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from .static_deployment_input_infra_reqs import StaticDeploymentInputInfraReqs
from .static_deployment_input_region_name import StaticDeploymentInputRegionName
from .static_deployment_input_users import StaticDeploymentInputUsers
from ..types import UNSET, Unset

T = TypeVar("T", bound="StaticDeploymentInput")


@attr.s(auto_attribs=True, repr=False, kw_only=True)
class StaticDeploymentInput:
    """
    Attributes:
        service (str): Service id or full name
        deployment_name (str): Deployment Name
        region_name (str): AWS supported region the deployment must be deployed in. Allowed values can be found in enum StaticDeploymentInputRegionName.
        is_dev_env (bool): Deployment Environment
        runtime_args (str): Run time arguments as a string
        users (dict): Dict of users
        infra_reqs (str): Infra request type. Allowed values can be found in enum StaticDeploymentInputInfraReqs.
        tags (Union[Unset, List[str]]):
    """

    service: str
    deployment_name: str
    region_name: str = attr.field(default=StaticDeploymentInputRegionName.US_EAST_1.value)
    is_dev_env: bool = attr.field(default=False)
    runtime_args: str = attr.field(default="")
    users: dict
    infra_reqs: str = attr.field(default=StaticDeploymentInputInfraReqs.M5_XLARGE.value)
    tags: Union[Unset, List[str]] = attr.field(default=[])
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __attrs_post_init__(self):
        """Creating Input for static service deployment

        Args:
            service (str): Service Id/name to be used (required)\n
            deployment_name (str): Name of the deployment (required)\n
            users (dict): Users of the deployment (required)\n
            region_name (str): AWS Region to be deployed in (Default - us-east-1)\n
            is_dev_env (bool): To be deployed in dev mode. (Default - False)\n
            infra_reqs (str): Infra to be used for deployment (Default - m5.xlarge)\n
            runtime_args (str): Runtime args in yaml string (Default - "")\n
            tags (list[str]): List of associated tags (Default - [])\n
            
        
        """
        self.users = StaticDeploymentInputUsers.from_dict(self.users)
        self.region_name = StaticDeploymentInputRegionName(self.region_name).value
        self.infra_reqs = StaticDeploymentInputInfraReqs(self.infra_reqs).value

    def to_dict(self) -> Dict[str, Any]:
        service = self.service
        deployment_name = self.deployment_name
        region_name = self.region_name

        is_dev_env = self.is_dev_env
        runtime_args = self.runtime_args
        users = self.users.to_dict()

        infra_reqs = self.infra_reqs

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags
        
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service": service,
                "deployment_name": deployment_name,
                "region_name": region_name,
                "is_dev_env": is_dev_env,
                "runtime_args": runtime_args,
                "users": users,
                "infra_reqs": infra_reqs,
            }
        )
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        service = d.pop("service")

        deployment_name = d.pop("deployment_name")

        region_name = StaticDeploymentInputRegionName(d.pop("region_name"))

        is_dev_env = d.pop("is_dev_env")

        runtime_args = d.pop("runtime_args")

        users = StaticDeploymentInputUsers.from_dict(d.pop("users"))

        infra_reqs = StaticDeploymentInputInfraReqs(d.pop("infra_reqs"))

        tags = cast(List[str], d.pop("tags", UNSET))

        static_deployment_input = cls(
            service=service,
            deployment_name=deployment_name,
            region_name=region_name,
            is_dev_env=is_dev_env,
            runtime_args=runtime_args,
            users=users,
            infra_reqs=infra_reqs,
            tags=tags,
        )

        static_deployment_input.additional_properties = d
        return static_deployment_input

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
