import json
from typing import Any, Dict, List, Type, TypeVar, cast

import attr
from .deployment_complete import DeploymentComplete

T = TypeVar("T", bound="AvailableDeployment")


@attr.s(auto_attribs=True, repr=False)
class AvailableDeployment:
    """
    Attributes:
        role (List[str]):
        deployment (DeploymentComplete):
    """

    role: List[str]
    deployment: "DeploymentComplete"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        role = self.role

        deployment = self.deployment.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "deployment": deployment,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        role = cast(List[str], d.pop("role"))

        deployment = DeploymentComplete.from_dict(d.pop("deployment"))

        available_deployment = cls(
            role=role,
            deployment=deployment,
        )

        available_deployment.additional_properties = d
        return available_deployment

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
