from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...exceptions import BadRequestError, HTTPClientError, ParamValidationError, UnauthorizedTokenError
from ...models.http_validation_error import HTTPValidationError
from ...models.message_model import MessageModel
from ...models.old_update_repo_service_repo_service_put_data import OldUpdateRepoServiceRepoServicePutData
from ...models.service_validation_response import ServiceValidationResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: OldUpdateRepoServiceRepoServicePutData,
    oblivious_user_id: str,
    repo_owner: str,
    repo_name: str,
    account_type: Union[Unset, None, str] = "github",
    ref: str,
    ref_type: Union[Unset, None, str] = "branch",
) -> Dict[str, Any]:
    url = "{}/repo/service".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["oblivious_user_id"] = oblivious_user_id

    params["repo_owner"] = repo_owner

    params["repo_name"] = repo_name

    params["account_type"] = account_type

    params["ref"] = ref

    params["ref_type"] = ref_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[HTTPValidationError, MessageModel, ServiceValidationResponse]]:
    if response.status_code == 200:
        response_200 = ServiceValidationResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400_message = response.json()["message"]
        raise BadRequestError(message=response_400_message)
    if response.status_code == 500:
        response_500_request_id = response.headers["apigw-requestid"]
        raise HTTPClientError(request_id=response_500_request_id)
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())
        if response_422.detail[0].type.__contains__("regex"):
            report = "Invalid " + response_422.detail[0].loc[-1] + " provided"
        report = "Invalid " + response_422.detail[0].loc[-1] + " provided"
        raise ParamValidationError(report=report)
    if response.status_code == 403:
        raise UnauthorizedTokenError()
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[HTTPValidationError, MessageModel, ServiceValidationResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: OldUpdateRepoServiceRepoServicePutData,
    oblivious_user_id: str,
    repo_owner: str,
    repo_name: str,
    account_type: Union[Unset, None, str] = "github",
    ref: str,
    ref_type: Union[Unset, None, str] = "branch",
) -> Response[Union[HTTPValidationError, MessageModel, ServiceValidationResponse]]:
    """Update Repo Services

     API to update a service. It fetches the current service.yaml file from VCS and validate it. It works
    in a similar way as Validate Repo Service API.

    This API is deprecated and will not be supported from upcoming releases. Kindly use **PUT
    /service/dynamic** for adding/updating dynamic services

    Args:
        oblivious_user_id (str): User id
        repo_owner (str): Repository owner for service
        repo_name (str): Repository name for service
        account_type (Union[Unset, None, str]): VCS type. Only supported input is github Default:
            'github'.
        ref (str): The reference tree of the repo
        ref_type (Union[Unset, None, str]): Whether the ref is a branch or tag Default: 'branch'.
        json_body (OldUpdateRepoServiceRepoServicePutData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, ServiceValidationResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        oblivious_user_id=oblivious_user_id,
        repo_owner=repo_owner,
        repo_name=repo_name,
        account_type=account_type,
        ref=ref,
        ref_type=ref_type,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: OldUpdateRepoServiceRepoServicePutData,
    oblivious_user_id: str,
    repo_owner: str,
    repo_name: str,
    account_type: Union[Unset, None, str] = "github",
    ref: str,
    ref_type: Union[Unset, None, str] = "branch",
) -> Optional[Union[HTTPValidationError, MessageModel, ServiceValidationResponse]]:
    """Update Repo Services

     API to update a service. It fetches the current service.yaml file from VCS and validate it. It works
    in a similar way as Validate Repo Service API.

    This API is deprecated and will not be supported from upcoming releases. Kindly use **PUT
    /service/dynamic** for adding/updating dynamic services

    Args:
        oblivious_user_id (str): User id
        repo_owner (str): Repository owner for service
        repo_name (str): Repository name for service
        account_type (Union[Unset, None, str]): VCS type. Only supported input is github Default:
            'github'.
        ref (str): The reference tree of the repo
        ref_type (Union[Unset, None, str]): Whether the ref is a branch or tag Default: 'branch'.
        json_body (OldUpdateRepoServiceRepoServicePutData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, ServiceValidationResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        oblivious_user_id=oblivious_user_id,
        repo_owner=repo_owner,
        repo_name=repo_name,
        account_type=account_type,
        ref=ref,
        ref_type=ref_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: OldUpdateRepoServiceRepoServicePutData,
    oblivious_user_id: str,
    repo_owner: str,
    repo_name: str,
    account_type: Union[Unset, None, str] = "github",
    ref: str,
    ref_type: Union[Unset, None, str] = "branch",
) -> Response[Union[HTTPValidationError, MessageModel, ServiceValidationResponse]]:
    """Update Repo Services

     API to update a service. It fetches the current service.yaml file from VCS and validate it. It works
    in a similar way as Validate Repo Service API.

    This API is deprecated and will not be supported from upcoming releases. Kindly use **PUT
    /service/dynamic** for adding/updating dynamic services

    Args:
        oblivious_user_id (str): User id
        repo_owner (str): Repository owner for service
        repo_name (str): Repository name for service
        account_type (Union[Unset, None, str]): VCS type. Only supported input is github Default:
            'github'.
        ref (str): The reference tree of the repo
        ref_type (Union[Unset, None, str]): Whether the ref is a branch or tag Default: 'branch'.
        json_body (OldUpdateRepoServiceRepoServicePutData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, ServiceValidationResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        oblivious_user_id=oblivious_user_id,
        repo_owner=repo_owner,
        repo_name=repo_name,
        account_type=account_type,
        ref=ref,
        ref_type=ref_type,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: OldUpdateRepoServiceRepoServicePutData,
    oblivious_user_id: str,
    repo_owner: str,
    repo_name: str,
    account_type: Union[Unset, None, str] = "github",
    ref: str,
    ref_type: Union[Unset, None, str] = "branch",
) -> Optional[Union[HTTPValidationError, MessageModel, ServiceValidationResponse]]:
    """Update Repo Services

     API to update a service. It fetches the current service.yaml file from VCS and validate it. It works
    in a similar way as Validate Repo Service API.

    This API is deprecated and will not be supported from upcoming releases. Kindly use **PUT
    /service/dynamic** for adding/updating dynamic services

    Args:
        oblivious_user_id (str): User id
        repo_owner (str): Repository owner for service
        repo_name (str): Repository name for service
        account_type (Union[Unset, None, str]): VCS type. Only supported input is github Default:
            'github'.
        ref (str): The reference tree of the repo
        ref_type (Union[Unset, None, str]): Whether the ref is a branch or tag Default: 'branch'.
        json_body (OldUpdateRepoServiceRepoServicePutData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, ServiceValidationResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            oblivious_user_id=oblivious_user_id,
            repo_owner=repo_owner,
            repo_name=repo_name,
            account_type=account_type,
            ref=ref,
            ref_type=ref_type,
        )
    ).parsed
