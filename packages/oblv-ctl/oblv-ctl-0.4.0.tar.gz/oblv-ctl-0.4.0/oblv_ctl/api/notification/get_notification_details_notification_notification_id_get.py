from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...exceptions import BadRequestError, HTTPClientError, ParamValidationError, UnauthorizedTokenError
from ...models.http_validation_error import HTTPValidationError
from ...models.message_model import MessageModel
from ...types import UNSET, Response


def _get_kwargs(
    notification_id: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
) -> Dict[str, Any]:
    url = "{}/notification/{notification_id}".format(client.base_url, notification_id=notification_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["oblivious_user_id"] = oblivious_user_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, HTTPValidationError, MessageModel, str]]:
    if response.status_code == 200:
        response_200 = cast(str, response.json())
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


def _build_response(*, response: httpx.Response) -> Response[Union[Any, HTTPValidationError, MessageModel, str]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    notification_id: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
) -> Response[Union[Any, HTTPValidationError, MessageModel, str]]:
    """Get Notification Details

    Args:
        notification_id (str):
        oblivious_user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MessageModel, str]
    """

    kwargs = _get_kwargs(
        notification_id=notification_id,
        client=client,
        oblivious_user_id=oblivious_user_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    notification_id: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
) -> Optional[Union[Any, HTTPValidationError, MessageModel, str]]:
    """Get Notification Details

    Args:
        notification_id (str):
        oblivious_user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MessageModel, str]
    """

    return sync_detailed(
        notification_id=notification_id,
        client=client,
        oblivious_user_id=oblivious_user_id,
    ).parsed


async def asyncio_detailed(
    notification_id: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
) -> Response[Union[Any, HTTPValidationError, MessageModel, str]]:
    """Get Notification Details

    Args:
        notification_id (str):
        oblivious_user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MessageModel, str]
    """

    kwargs = _get_kwargs(
        notification_id=notification_id,
        client=client,
        oblivious_user_id=oblivious_user_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    notification_id: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
) -> Optional[Union[Any, HTTPValidationError, MessageModel, str]]:
    """Get Notification Details

    Args:
        notification_id (str):
        oblivious_user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MessageModel, str]
    """

    return (
        await asyncio_detailed(
            notification_id=notification_id,
            client=client,
            oblivious_user_id=oblivious_user_id,
        )
    ).parsed
