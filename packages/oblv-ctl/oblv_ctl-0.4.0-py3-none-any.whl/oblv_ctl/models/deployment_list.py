import json
from typing import Any, Dict, List, Type, TypeVar

import attr
from .deployment_complete import DeploymentComplete

T = TypeVar("T", bound="DeploymentList")


@attr.s(auto_attribs=True, repr=False)
class DeploymentList:
    """
    Attributes:
        total_pages (int):
        deployments (List['DeploymentComplete']):
    """

    total_pages: int
    deployments: List["DeploymentComplete"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total_pages = self.total_pages
        deployments = []
        for deployments_item_data in self.deployments:
            deployments_item = deployments_item_data.to_dict()

            deployments.append(deployments_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_pages": total_pages,
                "deployments": deployments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        total_pages = d.pop("total_pages")

        deployments = []
        _deployments = d.pop("deployments")
        for deployments_item_data in _deployments:
            deployments_item = DeploymentComplete.from_dict(deployments_item_data)

            deployments.append(deployments_item)

        deployment_list = cls(
            total_pages=total_pages,
            deployments=deployments,
        )

        deployment_list.additional_properties = d
        return deployment_list

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
