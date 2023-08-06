from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...exceptions import AuthenticationError, BadRequestError, HTTPClientError, ParamValidationError
from ...models.api_key import APIKey
from ...models.http_validation_error import HTTPValidationError
from ...models.message_model import MessageModel
from ...models.oblv_auth_response import OblvAuthResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: APIKey,
) -> Dict[str, Any]:
    url = "{}/login/apikey".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[HTTPValidationError, MessageModel, OblvAuthResponse]]:
    if response.status_code == 200:
        response_200 = OblvAuthResponse.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        raise AuthenticationError()
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
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[HTTPValidationError, MessageModel, OblvAuthResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: APIKey,
) -> Response[Union[HTTPValidationError, MessageModel, OblvAuthResponse]]:
    """Authenticate With Apikey

     API to validate user's credentials using their **apikey**. This apikey is to be generated from the
    Console UI and then used for authentication.

    Args:
        json_body (APIKey):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, OblvAuthResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: APIKey,
) -> Optional[Union[HTTPValidationError, MessageModel, OblvAuthResponse]]:
    """Authenticate With Apikey

     API to validate user's credentials using their **apikey**. This apikey is to be generated from the
    Console UI and then used for authentication.

    Args:
        json_body (APIKey):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, OblvAuthResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: APIKey,
) -> Response[Union[HTTPValidationError, MessageModel, OblvAuthResponse]]:
    """Authenticate With Apikey

     API to validate user's credentials using their **apikey**. This apikey is to be generated from the
    Console UI and then used for authentication.

    Args:
        json_body (APIKey):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, OblvAuthResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: APIKey,
) -> Optional[Union[HTTPValidationError, MessageModel, OblvAuthResponse]]:
    """Authenticate With Apikey

     API to validate user's credentials using their **apikey**. This apikey is to be generated from the
    Console UI and then used for authentication.

    Args:
        json_body (APIKey):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, OblvAuthResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
