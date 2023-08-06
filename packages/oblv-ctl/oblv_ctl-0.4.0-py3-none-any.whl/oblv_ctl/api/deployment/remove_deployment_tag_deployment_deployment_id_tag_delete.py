from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...exceptions import BadRequestError, HTTPClientError, ParamValidationError, UnauthorizedTokenError
from ...models.http_validation_error import HTTPValidationError
from ...models.message_model import MessageModel
from ...types import UNSET, Response


def _get_kwargs(
    deployment_id: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    tag: str,
) -> Dict[str, Any]:
    url = "{}/deployment/{deployment_id}/tag".format(client.base_url, deployment_id=deployment_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["oblivious_user_id"] = oblivious_user_id

    params["tag"] = tag

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, MessageModel]]:
    if response.status_code == 200:
        response_200 = MessageModel.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, MessageModel]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    deployment_id: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    tag: str,
) -> Response[Union[HTTPValidationError, MessageModel]]:
    """Remove Deployment Tag

     API to remove a deployment's tag.

    Args:
        deployment_id (str):
        oblivious_user_id (str):
        tag (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel]
    """

    kwargs = _get_kwargs(
        deployment_id=deployment_id,
        client=client,
        oblivious_user_id=oblivious_user_id,
        tag=tag,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    deployment_id: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    tag: str,
) -> Optional[Union[HTTPValidationError, MessageModel]]:
    """Remove Deployment Tag

     API to remove a deployment's tag.

    Args:
        deployment_id (str):
        oblivious_user_id (str):
        tag (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel]
    """

    return sync_detailed(
        deployment_id=deployment_id,
        client=client,
        oblivious_user_id=oblivious_user_id,
        tag=tag,
    ).parsed


async def asyncio_detailed(
    deployment_id: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    tag: str,
) -> Response[Union[HTTPValidationError, MessageModel]]:
    """Remove Deployment Tag

     API to remove a deployment's tag.

    Args:
        deployment_id (str):
        oblivious_user_id (str):
        tag (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel]
    """

    kwargs = _get_kwargs(
        deployment_id=deployment_id,
        client=client,
        oblivious_user_id=oblivious_user_id,
        tag=tag,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    deployment_id: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    tag: str,
) -> Optional[Union[HTTPValidationError, MessageModel]]:
    """Remove Deployment Tag

     API to remove a deployment's tag.

    Args:
        deployment_id (str):
        oblivious_user_id (str):
        tag (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel]
    """

    return (
        await asyncio_detailed(
            deployment_id=deployment_id,
            client=client,
            oblivious_user_id=oblivious_user_id,
            tag=tag,
        )
    ).parsed
