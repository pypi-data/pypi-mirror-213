import json
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserCreditUtilization")


@attr.s(auto_attribs=True, repr=False)
class UserCreditUtilization:
    """
    Attributes:
        total_credits (Union[Unset, int]):
        total_running_deployments (Union[Unset, int]):
        esitmated_hours_remaining (Union[Unset, int]):
        hourly_credit_utilization (Union[Unset, int]):
    """

    total_credits: Union[Unset, int] = 0
    total_running_deployments: Union[Unset, int] = 0
    esitmated_hours_remaining: Union[Unset, int] = 0
    hourly_credit_utilization: Union[Unset, int] = 0
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total_credits = self.total_credits
        total_running_deployments = self.total_running_deployments
        esitmated_hours_remaining = self.esitmated_hours_remaining
        hourly_credit_utilization = self.hourly_credit_utilization

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if total_credits is not UNSET:
            field_dict["total_credits"] = total_credits
        if total_running_deployments is not UNSET:
            field_dict["total_running_deployments"] = total_running_deployments
        if esitmated_hours_remaining is not UNSET:
            field_dict["esitmated_hours_remaining"] = esitmated_hours_remaining
        if hourly_credit_utilization is not UNSET:
            field_dict["hourly_credit_utilization"] = hourly_credit_utilization

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        total_credits = d.pop("total_credits", UNSET)

        total_running_deployments = d.pop("total_running_deployments", UNSET)

        esitmated_hours_remaining = d.pop("esitmated_hours_remaining", UNSET)

        hourly_credit_utilization = d.pop("hourly_credit_utilization", UNSET)

        user_credit_utilization = cls(
            total_credits=total_credits,
            total_running_deployments=total_running_deployments,
            esitmated_hours_remaining=esitmated_hours_remaining,
            hourly_credit_utilization=hourly_credit_utilization,
        )

        user_credit_utilization.additional_properties = d
        return user_credit_utilization

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
