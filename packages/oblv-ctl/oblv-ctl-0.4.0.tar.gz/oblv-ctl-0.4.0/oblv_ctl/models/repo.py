import json
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Repo")


@attr.s(auto_attribs=True, repr=False)
class Repo:
    """
    Attributes:
        repo_id (Union[Unset, str]):  Default: ''.
        name (Union[Unset, str]):  Default: ''.
        full_name (Union[Unset, str]):  Default: ''.
        is_private (Union[Unset, bool]):
        owner_login (Union[Unset, str]):  Default: ''.
        description (Union[Unset, str]):  Default: ''.
        html_url (Union[Unset, str]):  Default: ''.
        git_url (Union[Unset, str]):  Default: ''.
        clone_url (Union[Unset, str]):  Default: ''.
        default_branch (Union[Unset, str]):  Default: ''.
        updated_at (Union[Unset, str]):  Default: ''.
        account_type (Union[Unset, str]):  Default: 'github'.
    """

    repo_id: Union[Unset, str] = ""
    name: Union[Unset, str] = ""
    full_name: Union[Unset, str] = ""
    is_private: Union[Unset, bool] = False
    owner_login: Union[Unset, str] = ""
    description: Union[Unset, str] = ""
    html_url: Union[Unset, str] = ""
    git_url: Union[Unset, str] = ""
    clone_url: Union[Unset, str] = ""
    default_branch: Union[Unset, str] = ""
    updated_at: Union[Unset, str] = ""
    account_type: Union[Unset, str] = "github"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        repo_id = self.repo_id
        name = self.name
        full_name = self.full_name
        is_private = self.is_private
        owner_login = self.owner_login
        description = self.description
        html_url = self.html_url
        git_url = self.git_url
        clone_url = self.clone_url
        default_branch = self.default_branch
        updated_at = self.updated_at
        account_type = self.account_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if repo_id is not UNSET:
            field_dict["repo_id"] = repo_id
        if name is not UNSET:
            field_dict["name"] = name
        if full_name is not UNSET:
            field_dict["full_name"] = full_name
        if is_private is not UNSET:
            field_dict["is_private"] = is_private
        if owner_login is not UNSET:
            field_dict["owner_login"] = owner_login
        if description is not UNSET:
            field_dict["description"] = description
        if html_url is not UNSET:
            field_dict["html_url"] = html_url
        if git_url is not UNSET:
            field_dict["git_url"] = git_url
        if clone_url is not UNSET:
            field_dict["clone_url"] = clone_url
        if default_branch is not UNSET:
            field_dict["default_branch"] = default_branch
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if account_type is not UNSET:
            field_dict["account_type"] = account_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        repo_id = d.pop("repo_id", UNSET)

        name = d.pop("name", UNSET)

        full_name = d.pop("full_name", UNSET)

        is_private = d.pop("is_private", UNSET)

        owner_login = d.pop("owner_login", UNSET)

        description = d.pop("description", UNSET)

        html_url = d.pop("html_url", UNSET)

        git_url = d.pop("git_url", UNSET)

        clone_url = d.pop("clone_url", UNSET)

        default_branch = d.pop("default_branch", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        account_type = d.pop("account_type", UNSET)

        repo = cls(
            repo_id=repo_id,
            name=name,
            full_name=full_name,
            is_private=is_private,
            owner_login=owner_login,
            description=description,
            html_url=html_url,
            git_url=git_url,
            clone_url=clone_url,
            default_branch=default_branch,
            updated_at=updated_at,
            account_type=account_type,
        )

        repo.additional_properties = d
        return repo

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
