import json
from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="PSK")


@attr.s(auto_attribs=True, repr=False)
class PSK:
    """
    Attributes:
        public_key (str): Publically shareable key
    """

    public_key: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        public_key = self.public_key

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "public_key": public_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        public_key = d.pop("public_key")

        psk = cls(
            public_key=public_key,
        )

        psk.additional_properties = d
        return psk

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
