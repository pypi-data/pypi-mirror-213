import json
from typing import Any, Dict, List, Type, TypeVar

import attr
from .user_static_service import UserStaticService

T = TypeVar("T", bound="UserServiceListUserStaticService")


@attr.s(auto_attribs=True, repr=False)
class UserServiceListUserStaticService:
    """Abstract base class for generic types.

    A generic type is typically declared by inheriting from
    this class parameterized with one or more type variables.
    For example, a generic mapping type might be defined as::

      class Mapping(Generic[KT, VT]):
          def __getitem__(self, key: KT) -> VT:
              ...
          # Etc.

    This class can then be used as follows::

      def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
          try:
              return mapping[key]
          except KeyError:
              return default

        Attributes:
            total_pages (int):
            services (List['UserStaticService']):
    """

    total_pages: int
    services: List["UserStaticService"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total_pages = self.total_pages
        services = []
        for services_item_data in self.services:
            services_item = services_item_data.to_dict()

            services.append(services_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_pages": total_pages,
                "services": services,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        total_pages = d.pop("total_pages")

        services = []
        _services = d.pop("services")
        for services_item_data in _services:
            services_item = UserStaticService.from_dict(services_item_data)

            services.append(services_item)

        user_service_list_user_static_service = cls(
            total_pages=total_pages,
            services=services,
        )

        user_service_list_user_static_service.additional_properties = d
        return user_service_list_user_static_service

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
