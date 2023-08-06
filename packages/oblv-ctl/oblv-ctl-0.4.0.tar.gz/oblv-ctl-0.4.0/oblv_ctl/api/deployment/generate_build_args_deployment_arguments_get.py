from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...exceptions import BadRequestError, HTTPClientError, ParamValidationError, UnauthorizedTokenError
from ...models.build_args_schema import BuildArgsSchema
from ...models.http_validation_error import HTTPValidationError
from ...models.message_model import MessageModel
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    owner: str,
    repo: str,
    ref: str,
    ref_type: Union[Unset, None, str] = "branch",
    account_type: Union[Unset, None, str] = "github",
) -> Dict[str, Any]:
    url = "{}/deployment/arguments".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["oblivious_user_id"] = oblivious_user_id

    params["owner"] = owner

    params["repo"] = repo

    params["ref"] = ref

    params["ref_type"] = ref_type

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[BuildArgsSchema, HTTPValidationError, MessageModel]]:
    if response.status_code == 200:
        response_200 = BuildArgsSchema.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400_message = response.json()["message"]
        raise BadRequestError(message=response_400_message)
    if response.status_code == 409:
        response_409 = MessageModel.from_dict(response.json())

        return response_409
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


def _build_response(*, response: httpx.Response) -> Response[Union[BuildArgsSchema, HTTPValidationError, MessageModel]]:
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
    owner: str,
    repo: str,
    ref: str,
    ref_type: Union[Unset, None, str] = "branch",
    account_type: Union[Unset, None, str] = "github",
) -> Response[Union[BuildArgsSchema, HTTPValidationError, MessageModel]]:
    """Get Build Deployment Arguments

     API to fetch the arguments schema necessary for creating a deployment. It also gives the commit sha,
    at which point it was generated. This is to be passed to the create deployment API.

    Note - A service could have different build args schema depending on the service's commit history.

    Args:
        oblivious_user_id (str):
        owner (str):
        repo (str):
        ref (str): Service Ref
        ref_type (Union[Unset, None, str]): Whether the ref is a branch or tag Default: 'branch'.
        account_type (Union[Unset, None, str]): VCS type. Only supported input is github Default:
            'github'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BuildArgsSchema, HTTPValidationError, MessageModel]
    """

    kwargs = _get_kwargs(
        client=client,
        oblivious_user_id=oblivious_user_id,
        owner=owner,
        repo=repo,
        ref=ref,
        ref_type=ref_type,
        account_type=account_type,
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
    owner: str,
    repo: str,
    ref: str,
    ref_type: Union[Unset, None, str] = "branch",
    account_type: Union[Unset, None, str] = "github",
) -> Optional[Union[BuildArgsSchema, HTTPValidationError, MessageModel]]:
    """Get Build Deployment Arguments

     API to fetch the arguments schema necessary for creating a deployment. It also gives the commit sha,
    at which point it was generated. This is to be passed to the create deployment API.

    Note - A service could have different build args schema depending on the service's commit history.

    Args:
        oblivious_user_id (str):
        owner (str):
        repo (str):
        ref (str): Service Ref
        ref_type (Union[Unset, None, str]): Whether the ref is a branch or tag Default: 'branch'.
        account_type (Union[Unset, None, str]): VCS type. Only supported input is github Default:
            'github'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BuildArgsSchema, HTTPValidationError, MessageModel]
    """

    return sync_detailed(
        client=client,
        oblivious_user_id=oblivious_user_id,
        owner=owner,
        repo=repo,
        ref=ref,
        ref_type=ref_type,
        account_type=account_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    owner: str,
    repo: str,
    ref: str,
    ref_type: Union[Unset, None, str] = "branch",
    account_type: Union[Unset, None, str] = "github",
) -> Response[Union[BuildArgsSchema, HTTPValidationError, MessageModel]]:
    """Get Build Deployment Arguments

     API to fetch the arguments schema necessary for creating a deployment. It also gives the commit sha,
    at which point it was generated. This is to be passed to the create deployment API.

    Note - A service could have different build args schema depending on the service's commit history.

    Args:
        oblivious_user_id (str):
        owner (str):
        repo (str):
        ref (str): Service Ref
        ref_type (Union[Unset, None, str]): Whether the ref is a branch or tag Default: 'branch'.
        account_type (Union[Unset, None, str]): VCS type. Only supported input is github Default:
            'github'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BuildArgsSchema, HTTPValidationError, MessageModel]
    """

    kwargs = _get_kwargs(
        client=client,
        oblivious_user_id=oblivious_user_id,
        owner=owner,
        repo=repo,
        ref=ref,
        ref_type=ref_type,
        account_type=account_type,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    owner: str,
    repo: str,
    ref: str,
    ref_type: Union[Unset, None, str] = "branch",
    account_type: Union[Unset, None, str] = "github",
) -> Optional[Union[BuildArgsSchema, HTTPValidationError, MessageModel]]:
    """Get Build Deployment Arguments

     API to fetch the arguments schema necessary for creating a deployment. It also gives the commit sha,
    at which point it was generated. This is to be passed to the create deployment API.

    Note - A service could have different build args schema depending on the service's commit history.

    Args:
        oblivious_user_id (str):
        owner (str):
        repo (str):
        ref (str): Service Ref
        ref_type (Union[Unset, None, str]): Whether the ref is a branch or tag Default: 'branch'.
        account_type (Union[Unset, None, str]): VCS type. Only supported input is github Default:
            'github'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BuildArgsSchema, HTTPValidationError, MessageModel]
    """

    return (
        await asyncio_detailed(
            client=client,
            oblivious_user_id=oblivious_user_id,
            owner=owner,
            repo=repo,
            ref=ref,
            ref_type=ref_type,
            account_type=account_type,
        )
    ).parsed
