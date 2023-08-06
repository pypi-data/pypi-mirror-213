from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...exceptions import BadRequestError, HTTPClientError, ParamValidationError, UnauthorizedTokenError
from ...models.http_validation_error import HTTPValidationError
from ...models.message_model import MessageModel
from ...models.repo import Repo
from ...types import UNSET, Response, Unset


def _get_kwargs(
    repo_owner: str,
    repo_name: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    account_type: Union[Unset, None, str] = "github",
) -> Dict[str, Any]:
    url = "{}/repo/{repo_owner}/{repo_name}".format(client.base_url, repo_owner=repo_owner, repo_name=repo_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["oblivious_user_id"] = oblivious_user_id

    params["account_type"] = account_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, MessageModel, Repo]]:
    if response.status_code == 200:
        response_200 = Repo.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, MessageModel, Repo]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    repo_owner: str,
    repo_name: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    account_type: Union[Unset, None, str] = "github",
) -> Response[Union[HTTPValidationError, MessageModel, Repo]]:
    """Get User Repo

     API to fetch user's repo information. This API is deprecated and will not be supported from upcoming
    releases. Kindly use GET /user/repo/{repo_owner}/{repo_name} for getting user's repo information.

    Args:
        repo_owner (str): Repository owner for service
        repo_name (str): Repository name for service
        oblivious_user_id (str): User id
        account_type (Union[Unset, None, str]): VCS type. Only supported input is github Default:
            'github'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, Repo]
    """

    kwargs = _get_kwargs(
        repo_owner=repo_owner,
        repo_name=repo_name,
        client=client,
        oblivious_user_id=oblivious_user_id,
        account_type=account_type,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    repo_owner: str,
    repo_name: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    account_type: Union[Unset, None, str] = "github",
) -> Optional[Union[HTTPValidationError, MessageModel, Repo]]:
    """Get User Repo

     API to fetch user's repo information. This API is deprecated and will not be supported from upcoming
    releases. Kindly use GET /user/repo/{repo_owner}/{repo_name} for getting user's repo information.

    Args:
        repo_owner (str): Repository owner for service
        repo_name (str): Repository name for service
        oblivious_user_id (str): User id
        account_type (Union[Unset, None, str]): VCS type. Only supported input is github Default:
            'github'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, Repo]
    """

    return sync_detailed(
        repo_owner=repo_owner,
        repo_name=repo_name,
        client=client,
        oblivious_user_id=oblivious_user_id,
        account_type=account_type,
    ).parsed


async def asyncio_detailed(
    repo_owner: str,
    repo_name: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    account_type: Union[Unset, None, str] = "github",
) -> Response[Union[HTTPValidationError, MessageModel, Repo]]:
    """Get User Repo

     API to fetch user's repo information. This API is deprecated and will not be supported from upcoming
    releases. Kindly use GET /user/repo/{repo_owner}/{repo_name} for getting user's repo information.

    Args:
        repo_owner (str): Repository owner for service
        repo_name (str): Repository name for service
        oblivious_user_id (str): User id
        account_type (Union[Unset, None, str]): VCS type. Only supported input is github Default:
            'github'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, Repo]
    """

    kwargs = _get_kwargs(
        repo_owner=repo_owner,
        repo_name=repo_name,
        client=client,
        oblivious_user_id=oblivious_user_id,
        account_type=account_type,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    repo_owner: str,
    repo_name: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    account_type: Union[Unset, None, str] = "github",
) -> Optional[Union[HTTPValidationError, MessageModel, Repo]]:
    """Get User Repo

     API to fetch user's repo information. This API is deprecated and will not be supported from upcoming
    releases. Kindly use GET /user/repo/{repo_owner}/{repo_name} for getting user's repo information.

    Args:
        repo_owner (str): Repository owner for service
        repo_name (str): Repository name for service
        oblivious_user_id (str): User id
        account_type (Union[Unset, None, str]): VCS type. Only supported input is github Default:
            'github'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, MessageModel, Repo]
    """

    return (
        await asyncio_detailed(
            repo_owner=repo_owner,
            repo_name=repo_name,
            client=client,
            oblivious_user_id=oblivious_user_id,
            account_type=account_type,
        )
    ).parsed
