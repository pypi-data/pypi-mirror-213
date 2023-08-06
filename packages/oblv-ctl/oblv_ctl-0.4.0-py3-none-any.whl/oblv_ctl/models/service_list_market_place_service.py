import json
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset
from .market_place_service import MarketPlaceService

T = TypeVar("T", bound="ServiceListMarketPlaceService")


@attr.s(auto_attribs=True, repr=False)
class ServiceListMarketPlaceService:
    """
    Attributes:
        total_pages (Union[Unset, int]):
        services (Union[Unset, List['MarketPlaceService']]):
    """

    total_pages: Union[Unset, int] = 0
    services: Union[Unset, List["MarketPlaceService"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        total_pages = self.total_pages
        services: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.services, Unset):
            services = []
            for services_item_data in self.services:
                services_item = services_item_data.to_dict()

                services.append(services_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if total_pages is not UNSET:
            field_dict["total_pages"] = total_pages
        if services is not UNSET:
            field_dict["services"] = services

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        total_pages = d.pop("total_pages", UNSET)

        services = []
        _services = d.pop("services", UNSET)
        for services_item_data in _services or []:
            services_item = MarketPlaceService.from_dict(services_item_data)

            services.append(services_item)

        service_list_market_place_service = cls(
            total_pages=total_pages,
            services=services,
        )

        return service_list_market_place_service
    
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