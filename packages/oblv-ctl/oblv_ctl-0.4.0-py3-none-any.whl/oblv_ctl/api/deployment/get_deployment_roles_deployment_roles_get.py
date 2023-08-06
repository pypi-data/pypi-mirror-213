from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...exceptions import BadRequestError, HTTPClientError, ParamValidationError, UnauthorizedTokenError
from ...models.http_validation_error import HTTPValidationError
from ...models.message_model import MessageModel
from ...models.role_response import RoleResponse
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    deployment_id: str,
) -> Dict[str, Any]:
    url = "{}/deployment/roles".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["oblivious_user_id"] = oblivious_user_id

    params["deployment_id"] = deployment_id

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
) -> Optional[Union[HTTPValidationError, List["RoleResponse"], MessageModel]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = RoleResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 400:
        response_400_message = response.json()["message"]
        raise BadRequestError(message=response_400_message)
    if response.status_code == 500:
        response_500_request_id = response.headers["apigw-requestid"]
        raise HTTPClientError(request_id=response_500_request_id)
    if response.status_code == 501:
        response_501 = MessageModel.from_dict(response.json())

        return response_501
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
) -> Response[Union[HTTPValidationError, List["RoleResponse"], MessageModel]]:
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
    deployment_id: str,
) -> Response[Union[HTTPValidationError, List["RoleResponse"], MessageModel]]:
    """Get Deployment Roles

     API to get a deployment's roles.

    Args:
        oblivious_user_id (str):
        deployment_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, List['RoleResponse'], MessageModel]
    """

    kwargs = _get_kwargs(
        client=client,
        oblivious_user_id=oblivious_user_id,
        deployment_id=deployment_id,
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
    deployment_id: str,
) -> Optional[Union[HTTPValidationError, List["RoleResponse"], MessageModel]]:
    """Get Deployment Roles

     API to get a deployment's roles.

    Args:
        oblivious_user_id (str):
        deployment_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, List['RoleResponse'], MessageModel]
    """

    return sync_detailed(
        client=client,
        oblivious_user_id=oblivious_user_id,
        deployment_id=deployment_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    deployment_id: str,
) -> Response[Union[HTTPValidationError, List["RoleResponse"], MessageModel]]:
    """Get Deployment Roles

     API to get a deployment's roles.

    Args:
        oblivious_user_id (str):
        deployment_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, List['RoleResponse'], MessageModel]
    """

    kwargs = _get_kwargs(
        client=client,
        oblivious_user_id=oblivious_user_id,
        deployment_id=deployment_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    deployment_id: str,
) -> Optional[Union[HTTPValidationError, List["RoleResponse"], MessageModel]]:
    """Get Deployment Roles

     API to get a deployment's roles.

    Args:
        oblivious_user_id (str):
        deployment_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, List['RoleResponse'], MessageModel]
    """

    return (
        await asyncio_detailed(
            client=client,
            oblivious_user_id=oblivious_user_id,
            deployment_id=deployment_id,
        )
    ).parsed
