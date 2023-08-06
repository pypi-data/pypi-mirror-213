from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...exceptions import BadRequestError, HTTPClientError, ParamValidationError, UnauthorizedTokenError
from ...models.http_validation_error import HTTPValidationError
from ...models.message_model import MessageModel
from ...models.service_list_market_place_service import ServiceListMarketPlaceService
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    page: Union[Unset, None, int] = 1,
    per_page: Union[Unset, None, int] = 10,
    get_all: Union[Unset, None, bool] = False,
    name_filter: Union[Unset, None, str] = "",
    repo_filter: Union[Unset, None, str] = "",
    owner_filter: Union[Unset, None, str] = "",
) -> Dict[str, Any]:
    url = "{}/service/marketplace".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["oblivious_user_id"] = oblivious_user_id

    params["page"] = page

    params["per_page"] = per_page

    params["get_all"] = get_all

    params["name_filter"] = name_filter

    params["repo_filter"] = repo_filter

    params["owner_filter"] = owner_filter

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
) -> Optional[Union[HTTPValidationError, MessageModel, ServiceListMarketPlaceService]]:
    if response.status_code == 200:
        response_200 = ServiceListMarketPlaceService.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, MessageModel, ServiceListMarketPlaceService]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    page: Union[Unset, None, int] = 1,
    per_page: Union[Unset, None, int] = 10,
    get_all: Union[Unset, None, bool] = False,
    name_filter: Union[Unset, None, str] = "",
    repo_filter: Union[Unset, None, str] = "",
    owner_filter: Union[Unset, None, str] = "",
) -> Response[Union[HTTPValidationError, MessageModel, ServiceListMarketPlaceService]]:
    """Get marketplace services

     To get all the marketplace services. These are the static services publically available for
    everyone's use.

    Args:
        oblivious_user_id (str): User id
        page (Union[Unset, None, int]): Requested page Default: 1.
        per_page (Union[Unset, None, int]): Responses per page Default: 10.
        get_all (Union[Unset, None, bool]): Get all responses. Precedence over *page* and
            *per_page* parameters
        name_filter (Union[Unset, None, str]): Name filter for services Default: ''.
        repo_filter (Union[Unset, None, str]): Repo filter for services Default: ''.
        owner_filter (Union[Unset, None, str]): Owner name filter for services Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, ServiceListMarketPlaceService]
    """

    kwargs = _get_kwargs(
        client=client,
        oblivious_user_id=oblivious_user_id,
        page=page,
        per_page=per_page,
        get_all=get_all,
        name_filter=name_filter,
        repo_filter=repo_filter,
        owner_filter=owner_filter,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    page: Union[Unset, None, int] = 1,
    per_page: Union[Unset, None, int] = 10,
    get_all: Union[Unset, None, bool] = False,
    name_filter: Union[Unset, None, str] = "",
    repo_filter: Union[Unset, None, str] = "",
    owner_filter: Union[Unset, None, str] = "",
) -> Optional[Union[HTTPValidationError, MessageModel, ServiceListMarketPlaceService]]:
    """Get marketplace services

     To get all the marketplace services. These are the static services publically available for
    everyone's use.

    Args:
        oblivious_user_id (str): User id
        page (Union[Unset, None, int]): Requested page Default: 1.
        per_page (Union[Unset, None, int]): Responses per page Default: 10.
        get_all (Union[Unset, None, bool]): Get all responses. Precedence over *page* and
            *per_page* parameters
        name_filter (Union[Unset, None, str]): Name filter for services Default: ''.
        repo_filter (Union[Unset, None, str]): Repo filter for services Default: ''.
        owner_filter (Union[Unset, None, str]): Owner name filter for services Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, ServiceListMarketPlaceService]
    """

    return sync_detailed(
        client=client,
        oblivious_user_id=oblivious_user_id,
        page=page,
        per_page=per_page,
        get_all=get_all,
        name_filter=name_filter,
        repo_filter=repo_filter,
        owner_filter=owner_filter,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    page: Union[Unset, None, int] = 1,
    per_page: Union[Unset, None, int] = 10,
    get_all: Union[Unset, None, bool] = False,
    name_filter: Union[Unset, None, str] = "",
    repo_filter: Union[Unset, None, str] = "",
    owner_filter: Union[Unset, None, str] = "",
) -> Response[Union[HTTPValidationError, MessageModel, ServiceListMarketPlaceService]]:
    """Get marketplace services

     To get all the marketplace services. These are the static services publically available for
    everyone's use.

    Args:
        oblivious_user_id (str): User id
        page (Union[Unset, None, int]): Requested page Default: 1.
        per_page (Union[Unset, None, int]): Responses per page Default: 10.
        get_all (Union[Unset, None, bool]): Get all responses. Precedence over *page* and
            *per_page* parameters
        name_filter (Union[Unset, None, str]): Name filter for services Default: ''.
        repo_filter (Union[Unset, None, str]): Repo filter for services Default: ''.
        owner_filter (Union[Unset, None, str]): Owner name filter for services Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, ServiceListMarketPlaceService]
    """

    kwargs = _get_kwargs(
        client=client,
        oblivious_user_id=oblivious_user_id,
        page=page,
        per_page=per_page,
        get_all=get_all,
        name_filter=name_filter,
        repo_filter=repo_filter,
        owner_filter=owner_filter,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    page: Union[Unset, None, int] = 1,
    per_page: Union[Unset, None, int] = 10,
    get_all: Union[Unset, None, bool] = False,
    name_filter: Union[Unset, None, str] = "",
    repo_filter: Union[Unset, None, str] = "",
    owner_filter: Union[Unset, None, str] = "",
) -> Optional[Union[HTTPValidationError, MessageModel, ServiceListMarketPlaceService]]:
    """Get marketplace services

     To get all the marketplace services. These are the static services publically available for
    everyone's use.

    Args:
        oblivious_user_id (str): User id
        page (Union[Unset, None, int]): Requested page Default: 1.
        per_page (Union[Unset, None, int]): Responses per page Default: 10.
        get_all (Union[Unset, None, bool]): Get all responses. Precedence over *page* and
            *per_page* parameters
        name_filter (Union[Unset, None, str]): Name filter for services Default: ''.
        repo_filter (Union[Unset, None, str]): Repo filter for services Default: ''.
        owner_filter (Union[Unset, None, str]): Owner name filter for services Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, ServiceListMarketPlaceService]
    """

    return (
        await asyncio_detailed(
            client=client,
            oblivious_user_id=oblivious_user_id,
            page=page,
            per_page=per_page,
            get_all=get_all,
            name_filter=name_filter,
            repo_filter=repo_filter,
            owner_filter=owner_filter,
        )
    ).parsed
