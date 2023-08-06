import json
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset
from .instance import Instance
from .shared_users import SharedUsers

T = TypeVar("T", bound="DeploymentResponse")


@attr.s(auto_attribs=True, repr=False)
class DeploymentResponse:
    """
    Attributes:
        deployment_id (Union[Unset, str]):  Default: ''.
        deployment_name (Union[Unset, str]):  Default: ''.
        owner_login (Union[Unset, str]):  Default: ''.
        repo_name (Union[Unset, str]):  Default: ''.
        account_type (Union[Unset, str]):  Default: ''.
        repo_owner (Union[Unset, str]):  Default: ''.
        tags (Union[Unset, List[str]]):
        branch_release (Union[Unset, str]):  Default: ''.
        current_state (Union[Unset, str]):  Default: ''.
        visibility (Union[Unset, str]):  Default: ''.
        is_dev_env (Union[Unset, bool]):  Default: True.
        pcr_codes (Union[Unset, List[str]]):
        credit_utilization_per_hour (Union[Unset, float]):
        creation_time (Union[Unset, str]):  Default: ''.
        sha (Union[Unset, str]):  Default: ''.
        is_deleted (Union[Unset, bool]):
        build_args (Union[Unset, Any]):
        instance (Union[Unset, Instance]):
        shared_users (Union[Unset, List['SharedUsers']]):
    """

    deployment_id: Union[Unset, str] = ""
    deployment_name: Union[Unset, str] = ""
    owner_login: Union[Unset, str] = ""
    repo_name: Union[Unset, str] = ""
    account_type: Union[Unset, str] = ""
    repo_owner: Union[Unset, str] = ""
    tags: Union[Unset, List[str]] = UNSET
    branch_release: Union[Unset, str] = ""
    current_state: Union[Unset, str] = ""
    visibility: Union[Unset, str] = ""
    is_dev_env: Union[Unset, bool] = True
    pcr_codes: Union[Unset, List[str]] = UNSET
    credit_utilization_per_hour: Union[Unset, float] = 0.0
    creation_time: Union[Unset, str] = ""
    sha: Union[Unset, str] = ""
    is_deleted: Union[Unset, bool] = False
    build_args: Union[Unset, Any] = UNSET
    instance: Union[Unset, "Instance"] = UNSET
    shared_users: Union[Unset, List["SharedUsers"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        deployment_id = self.deployment_id
        deployment_name = self.deployment_name
        owner_login = self.owner_login
        repo_name = self.repo_name
        account_type = self.account_type
        repo_owner = self.repo_owner
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        branch_release = self.branch_release
        current_state = self.current_state
        visibility = self.visibility
        is_dev_env = self.is_dev_env
        pcr_codes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.pcr_codes, Unset):
            pcr_codes = self.pcr_codes

        credit_utilization_per_hour = self.credit_utilization_per_hour
        creation_time = self.creation_time
        sha = self.sha
        is_deleted = self.is_deleted
        build_args = self.build_args
        instance: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.instance, Unset):
            instance = self.instance.to_dict()

        shared_users: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.shared_users, Unset):
            shared_users = []
            for shared_users_item_data in self.shared_users:
                shared_users_item = shared_users_item_data.to_dict()

                shared_users.append(shared_users_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if deployment_id is not UNSET:
            field_dict["deployment_id"] = deployment_id
        if deployment_name is not UNSET:
            field_dict["deployment_name"] = deployment_name
        if owner_login is not UNSET:
            field_dict["owner_login"] = owner_login
        if repo_name is not UNSET:
            field_dict["repo_name"] = repo_name
        if account_type is not UNSET:
            field_dict["account_type"] = account_type
        if repo_owner is not UNSET:
            field_dict["repo_owner"] = repo_owner
        if tags is not UNSET:
            field_dict["tags"] = tags
        if branch_release is not UNSET:
            field_dict["branch_release"] = branch_release
        if current_state is not UNSET:
            field_dict["current_state"] = current_state
        if visibility is not UNSET:
            field_dict["visibility"] = visibility
        if is_dev_env is not UNSET:
            field_dict["is_dev_env"] = is_dev_env
        if pcr_codes is not UNSET:
            field_dict["pcr_codes"] = pcr_codes
        if credit_utilization_per_hour is not UNSET:
            field_dict["credit_utilization_per_hour"] = credit_utilization_per_hour
        if creation_time is not UNSET:
            field_dict["creation_time"] = creation_time
        if sha is not UNSET:
            field_dict["sha"] = sha
        if is_deleted is not UNSET:
            field_dict["is_deleted"] = is_deleted
        if build_args is not UNSET:
            field_dict["build_args"] = build_args
        if instance is not UNSET:
            field_dict["instance"] = instance
        if shared_users is not UNSET:
            field_dict["shared_users"] = shared_users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        deployment_id = d.pop("deployment_id", UNSET)

        deployment_name = d.pop("deployment_name", UNSET)

        owner_login = d.pop("owner_login", UNSET)

        repo_name = d.pop("repo_name", UNSET)

        account_type = d.pop("account_type", UNSET)

        repo_owner = d.pop("repo_owner", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        branch_release = d.pop("branch_release", UNSET)

        current_state = d.pop("current_state", UNSET)

        visibility = d.pop("visibility", UNSET)

        is_dev_env = d.pop("is_dev_env", UNSET)

        pcr_codes = cast(List[str], d.pop("pcr_codes", UNSET))

        credit_utilization_per_hour = d.pop("credit_utilization_per_hour", UNSET)

        creation_time = d.pop("creation_time", UNSET)

        sha = d.pop("sha", UNSET)

        is_deleted = d.pop("is_deleted", UNSET)

        build_args = d.pop("build_args", UNSET)

        _instance = d.pop("instance", UNSET)
        instance: Union[Unset, Instance]
        if isinstance(_instance, Unset):
            instance = UNSET
        else:
            instance = Instance.from_dict(_instance)

        shared_users = []
        _shared_users = d.pop("shared_users", UNSET)
        for shared_users_item_data in _shared_users or []:
            shared_users_item = SharedUsers.from_dict(shared_users_item_data)

            shared_users.append(shared_users_item)

        deployment_response = cls(
            deployment_id=deployment_id,
            deployment_name=deployment_name,
            owner_login=owner_login,
            repo_name=repo_name,
            account_type=account_type,
            repo_owner=repo_owner,
            tags=tags,
            branch_release=branch_release,
            current_state=current_state,
            visibility=visibility,
            is_dev_env=is_dev_env,
            pcr_codes=pcr_codes,
            credit_utilization_per_hour=credit_utilization_per_hour,
            creation_time=creation_time,
            sha=sha,
            is_deleted=is_deleted,
            build_args=build_args,
            instance=instance,
            shared_users=shared_users,
        )

        deployment_response.additional_properties = d
        return deployment_response

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
