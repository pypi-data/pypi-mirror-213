from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...exceptions import BadRequestError, HTTPClientError, ParamValidationError, UnauthorizedTokenError
from ...models.http_validation_error import HTTPValidationError
from ...models.message_model import MessageModel
from ...models.service_list_repo_dynamic_service import ServiceListRepoDynamicService
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    account_type: Union[Unset, None, str] = "github",
    page: Union[Unset, None, int] = 1,
    per_page: Union[Unset, None, int] = 10,
    get_all: Union[Unset, None, bool] = False,
    oblivious_user_id: str,
    repo_owner: str,
    repo_name: str,
) -> Dict[str, Any]:
    url = "{}/repo/service".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["account_type"] = account_type

    params["page"] = page

    params["per_page"] = per_page

    params["get_all"] = get_all

    params["oblivious_user_id"] = oblivious_user_id

    params["repo_owner"] = repo_owner

    params["repo_name"] = repo_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[HTTPValidationError, MessageModel, ServiceListRepoDynamicService]]:
    if response.status_code == 200:
        response_200 = ServiceListRepoDynamicService.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, MessageModel, ServiceListRepoDynamicService]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    account_type: Union[Unset, None, str] = "github",
    page: Union[Unset, None, int] = 1,
    per_page: Union[Unset, None, int] = 10,
    get_all: Union[Unset, None, bool] = False,
    oblivious_user_id: str,
    repo_owner: str,
    repo_name: str,
) -> Response[Union[HTTPValidationError, MessageModel, ServiceListRepoDynamicService]]:
    """Get Repo Services

     API to fetch all the services available for the given repository. This API is valid only for linked
    repositories. This API is deprecated and will not be supported from upcoming releases. Kindly use
    GET /repo/service/dynamic for list of dynamic services

    Args:
        account_type (Union[Unset, None, str]): VCS type. Only supported input is github Default:
            'github'.
        page (Union[Unset, None, int]): Requested page Default: 1.
        per_page (Union[Unset, None, int]): Responses per page Default: 10.
        get_all (Union[Unset, None, bool]): Get all responses. Precedence over *page* and
            *per_page* parameters
        oblivious_user_id (str): User id
        repo_owner (str): Repository owner for service
        repo_name (str): Repository name for service

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, ServiceListRepoDynamicService]
    """

    kwargs = _get_kwargs(
        client=client,
        account_type=account_type,
        page=page,
        per_page=per_page,
        get_all=get_all,
        oblivious_user_id=oblivious_user_id,
        repo_owner=repo_owner,
        repo_name=repo_name,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    account_type: Union[Unset, None, str] = "github",
    page: Union[Unset, None, int] = 1,
    per_page: Union[Unset, None, int] = 10,
    get_all: Union[Unset, None, bool] = False,
    oblivious_user_id: str,
    repo_owner: str,
    repo_name: str,
) -> Optional[Union[HTTPValidationError, MessageModel, ServiceListRepoDynamicService]]:
    """Get Repo Services

     API to fetch all the services available for the given repository. This API is valid only for linked
    repositories. This API is deprecated and will not be supported from upcoming releases. Kindly use
    GET /repo/service/dynamic for list of dynamic services

    Args:
        account_type (Union[Unset, None, str]): VCS type. Only supported input is github Default:
            'github'.
        page (Union[Unset, None, int]): Requested page Default: 1.
        per_page (Union[Unset, None, int]): Responses per page Default: 10.
        get_all (Union[Unset, None, bool]): Get all responses. Precedence over *page* and
            *per_page* parameters
        oblivious_user_id (str): User id
        repo_owner (str): Repository owner for service
        repo_name (str): Repository name for service

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, ServiceListRepoDynamicService]
    """

    return sync_detailed(
        client=client,
        account_type=account_type,
        page=page,
        per_page=per_page,
        get_all=get_all,
        oblivious_user_id=oblivious_user_id,
        repo_owner=repo_owner,
        repo_name=repo_name,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    account_type: Union[Unset, None, str] = "github",
    page: Union[Unset, None, int] = 1,
    per_page: Union[Unset, None, int] = 10,
    get_all: Union[Unset, None, bool] = False,
    oblivious_user_id: str,
    repo_owner: str,
    repo_name: str,
) -> Response[Union[HTTPValidationError, MessageModel, ServiceListRepoDynamicService]]:
    """Get Repo Services

     API to fetch all the services available for the given repository. This API is valid only for linked
    repositories. This API is deprecated and will not be supported from upcoming releases. Kindly use
    GET /repo/service/dynamic for list of dynamic services

    Args:
        account_type (Union[Unset, None, str]): VCS type. Only supported input is github Default:
            'github'.
        page (Union[Unset, None, int]): Requested page Default: 1.
        per_page (Union[Unset, None, int]): Responses per page Default: 10.
        get_all (Union[Unset, None, bool]): Get all responses. Precedence over *page* and
            *per_page* parameters
        oblivious_user_id (str): User id
        repo_owner (str): Repository owner for service
        repo_name (str): Repository name for service

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, ServiceListRepoDynamicService]
    """

    kwargs = _get_kwargs(
        client=client,
        account_type=account_type,
        page=page,
        per_page=per_page,
        get_all=get_all,
        oblivious_user_id=oblivious_user_id,
        repo_owner=repo_owner,
        repo_name=repo_name,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    account_type: Union[Unset, None, str] = "github",
    page: Union[Unset, None, int] = 1,
    per_page: Union[Unset, None, int] = 10,
    get_all: Union[Unset, None, bool] = False,
    oblivious_user_id: str,
    repo_owner: str,
    repo_name: str,
) -> Optional[Union[HTTPValidationError, MessageModel, ServiceListRepoDynamicService]]:
    """Get Repo Services

     API to fetch all the services available for the given repository. This API is valid only for linked
    repositories. This API is deprecated and will not be supported from upcoming releases. Kindly use
    GET /repo/service/dynamic for list of dynamic services

    Args:
        account_type (Union[Unset, None, str]): VCS type. Only supported input is github Default:
            'github'.
        page (Union[Unset, None, int]): Requested page Default: 1.
        per_page (Union[Unset, None, int]): Responses per page Default: 10.
        get_all (Union[Unset, None, bool]): Get all responses. Precedence over *page* and
            *per_page* parameters
        oblivious_user_id (str): User id
        repo_owner (str): Repository owner for service
        repo_name (str): Repository name for service

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, ServiceListRepoDynamicService]
    """

    return (
        await asyncio_detailed(
            client=client,
            account_type=account_type,
            page=page,
            per_page=per_page,
            get_all=get_all,
            oblivious_user_id=oblivious_user_id,
            repo_owner=repo_owner,
            repo_name=repo_name,
        )
    ).parsed
