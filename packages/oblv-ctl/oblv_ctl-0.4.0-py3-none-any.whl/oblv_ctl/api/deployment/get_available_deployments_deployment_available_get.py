from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...exceptions import BadRequestError, HTTPClientError, ParamValidationError, UnauthorizedTokenError
from ...models.available_deployment_list import AvailableDeploymentList
from ...models.http_validation_error import HTTPValidationError
from ...models.message_model import MessageModel
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    page: Union[Unset, None, int] = 1,
    per_page: Union[Unset, None, int] = 10,
    search_term: Union[Unset, None, str] = "",
) -> Dict[str, Any]:
    url = "{}/deployment/available".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["oblivious_user_id"] = oblivious_user_id

    params["page"] = page

    params["per_page"] = per_page

    params["search_term"] = search_term

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
) -> Optional[Union[AvailableDeploymentList, HTTPValidationError, MessageModel]]:
    if response.status_code == 200:
        response_200 = AvailableDeploymentList.from_dict(response.json())

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
) -> Response[Union[AvailableDeploymentList, HTTPValidationError, MessageModel]]:
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
) -> Response[Union[AvailableDeploymentList, HTTPValidationError, MessageModel]]:
    """Get Available Deployments

     API to fetch all the deployments the user can connect to.

    Args:
        oblivious_user_id (str):
        page (Union[Unset, None, int]):  Default: 1.
        per_page (Union[Unset, None, int]):  Default: 10.
        search_term (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AvailableDeploymentList, HTTPValidationError, MessageModel]
    """

    kwargs = _get_kwargs(
        client=client,
        oblivious_user_id=oblivious_user_id,
        page=page,
        per_page=per_page,
        search_term=search_term,
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
) -> Optional[Union[AvailableDeploymentList, HTTPValidationError, MessageModel]]:
    """Get Available Deployments

     API to fetch all the deployments the user can connect to.

    Args:
        oblivious_user_id (str):
        page (Union[Unset, None, int]):  Default: 1.
        per_page (Union[Unset, None, int]):  Default: 10.
        search_term (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AvailableDeploymentList, HTTPValidationError, MessageModel]
    """

    return sync_detailed(
        client=client,
        oblivious_user_id=oblivious_user_id,
        page=page,
        per_page=per_page,
        search_term=search_term,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    page: Union[Unset, None, int] = 1,
    per_page: Union[Unset, None, int] = 10,
    search_term: Union[Unset, None, str] = "",
) -> Response[Union[AvailableDeploymentList, HTTPValidationError, MessageModel]]:
    """Get Available Deployments

     API to fetch all the deployments the user can connect to.

    Args:
        oblivious_user_id (str):
        page (Union[Unset, None, int]):  Default: 1.
        per_page (Union[Unset, None, int]):  Default: 10.
        search_term (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AvailableDeploymentList, HTTPValidationError, MessageModel]
    """

    kwargs = _get_kwargs(
        client=client,
        oblivious_user_id=oblivious_user_id,
        page=page,
        per_page=per_page,
        search_term=search_term,
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
) -> Optional[Union[AvailableDeploymentList, HTTPValidationError, MessageModel]]:
    """Get Available Deployments

     API to fetch all the deployments the user can connect to.

    Args:
        oblivious_user_id (str):
        page (Union[Unset, None, int]):  Default: 1.
        per_page (Union[Unset, None, int]):  Default: 10.
        search_term (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AvailableDeploymentList, HTTPValidationError, MessageModel]
    """

    return (
        await asyncio_detailed(
            client=client,
            oblivious_user_id=oblivious_user_id,
            page=page,
            per_page=per_page,
            search_term=search_term,
        )
    ).parsed
