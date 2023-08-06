from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...exceptions import BadRequestError, HTTPClientError, ParamValidationError, UnauthorizedTokenError
from ...models.http_validation_error import HTTPValidationError
from ...models.message_model import MessageModel
from ...models.user_service_list_user_dynamic_service import UserServiceListUserDynamicService
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    page: Union[Unset, None, int] = 1,
    per_page: Union[Unset, None, int] = 10,
    search_term: Union[Unset, None, str] = "",
    get_all: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/user/service/dynamic".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["oblivious_user_id"] = oblivious_user_id

    params["page"] = page

    params["per_page"] = per_page

    params["search_term"] = search_term

    params["get_all"] = get_all

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
) -> Optional[Union[Any, HTTPValidationError, MessageModel, UserServiceListUserDynamicService]]:
    if response.status_code == 200:
        response_200 = UserServiceListUserDynamicService.from_dict(response.json())

        return response_200
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
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
) -> Response[Union[Any, HTTPValidationError, MessageModel, UserServiceListUserDynamicService]]:
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
    search_term: Union[Unset, None, str] = "",
    get_all: Union[Unset, None, bool] = False,
) -> Response[Union[Any, HTTPValidationError, MessageModel, UserServiceListUserDynamicService]]:
    """Get user dynamic services

     To fetch all dynamic services owned by the user. These are equivalent to the services in the
    previous version.

    Args:
        oblivious_user_id (str): User id
        page (Union[Unset, None, int]): Requested page Default: 1.
        per_page (Union[Unset, None, int]): Responses per page Default: 10.
        search_term (Union[Unset, None, str]): Search keyword for resources to be filtered with
            Default: ''.
        get_all (Union[Unset, None, bool]): Get all responses. Precedence over *page* and
            *per_page* parameters

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MessageModel, UserServiceListUserDynamicService]
    """

    kwargs = _get_kwargs(
        client=client,
        oblivious_user_id=oblivious_user_id,
        page=page,
        per_page=per_page,
        search_term=search_term,
        get_all=get_all,
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
    search_term: Union[Unset, None, str] = "",
    get_all: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, HTTPValidationError, MessageModel, UserServiceListUserDynamicService]]:
    """Get user dynamic services

     To fetch all dynamic services owned by the user. These are equivalent to the services in the
    previous version.

    Args:
        oblivious_user_id (str): User id
        page (Union[Unset, None, int]): Requested page Default: 1.
        per_page (Union[Unset, None, int]): Responses per page Default: 10.
        search_term (Union[Unset, None, str]): Search keyword for resources to be filtered with
            Default: ''.
        get_all (Union[Unset, None, bool]): Get all responses. Precedence over *page* and
            *per_page* parameters

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MessageModel, UserServiceListUserDynamicService]
    """

    return sync_detailed(
        client=client,
        oblivious_user_id=oblivious_user_id,
        page=page,
        per_page=per_page,
        search_term=search_term,
        get_all=get_all,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    page: Union[Unset, None, int] = 1,
    per_page: Union[Unset, None, int] = 10,
    search_term: Union[Unset, None, str] = "",
    get_all: Union[Unset, None, bool] = False,
) -> Response[Union[Any, HTTPValidationError, MessageModel, UserServiceListUserDynamicService]]:
    """Get user dynamic services

     To fetch all dynamic services owned by the user. These are equivalent to the services in the
    previous version.

    Args:
        oblivious_user_id (str): User id
        page (Union[Unset, None, int]): Requested page Default: 1.
        per_page (Union[Unset, None, int]): Responses per page Default: 10.
        search_term (Union[Unset, None, str]): Search keyword for resources to be filtered with
            Default: ''.
        get_all (Union[Unset, None, bool]): Get all responses. Precedence over *page* and
            *per_page* parameters

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MessageModel, UserServiceListUserDynamicService]
    """

    kwargs = _get_kwargs(
        client=client,
        oblivious_user_id=oblivious_user_id,
        page=page,
        per_page=per_page,
        search_term=search_term,
        get_all=get_all,
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
    search_term: Union[Unset, None, str] = "",
    get_all: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, HTTPValidationError, MessageModel, UserServiceListUserDynamicService]]:
    """Get user dynamic services

     To fetch all dynamic services owned by the user. These are equivalent to the services in the
    previous version.

    Args:
        oblivious_user_id (str): User id
        page (Union[Unset, None, int]): Requested page Default: 1.
        per_page (Union[Unset, None, int]): Responses per page Default: 10.
        search_term (Union[Unset, None, str]): Search keyword for resources to be filtered with
            Default: ''.
        get_all (Union[Unset, None, bool]): Get all responses. Precedence over *page* and
            *per_page* parameters

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MessageModel, UserServiceListUserDynamicService]
    """

    return (
        await asyncio_detailed(
            client=client,
            oblivious_user_id=oblivious_user_id,
            page=page,
            per_page=per_page,
            search_term=search_term,
            get_all=get_all,
        )
    ).parsed
