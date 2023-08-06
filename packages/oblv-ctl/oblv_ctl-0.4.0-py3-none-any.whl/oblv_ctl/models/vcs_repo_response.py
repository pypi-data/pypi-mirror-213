import json
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from .repo import Repo
from ..types import UNSET, Unset

T = TypeVar("T", bound="VCSRepoResponse")


@attr.s(auto_attribs=True, repr=False)
class VCSRepoResponse:
    """
    Attributes:
        repos (Union[Unset, List['Repo']]):
        total_pages (Union[Unset, int]):
        message (Union[Unset, str]):  Default: ''.
    """

    repos: Union[Unset, List["Repo"]] = UNSET
    total_pages: Union[Unset, int] = 0
    message: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        repos: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.repos, Unset):
            repos = []
            for repos_item_data in self.repos:
                repos_item = repos_item_data.to_dict()

                repos.append(repos_item)

        total_pages = self.total_pages
        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if repos is not UNSET:
            field_dict["repos"] = repos
        if total_pages is not UNSET:
            field_dict["total_pages"] = total_pages
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        repos = []
        _repos = d.pop("repos", UNSET)
        for repos_item_data in _repos or []:
            repos_item = Repo.from_dict(repos_item_data)

            repos.append(repos_item)

        total_pages = d.pop("total_pages", UNSET)

        message = d.pop("message", UNSET)

        vcs_repo_response = cls(
            repos=repos,
            total_pages=total_pages,
            message=message,
        )

        vcs_repo_response.additional_properties = d
        return vcs_repo_response

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
