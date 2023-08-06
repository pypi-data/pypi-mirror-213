from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.patched_task import PatchedTask
from ...models.task import Task
from ...types import Response


def _get_kwargs(
    task_id: str,
    *,
    client: AuthenticatedClient,
    json_body: PatchedTask,
) -> Dict[str, Any]:
    url = "{}/api/tasks/{task_id}/".format(client.base_url, task_id=task_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "patch",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Task]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Task.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Task]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    task_id: str,
    *,
    client: AuthenticatedClient,
    json_body: PatchedTask,
) -> Response[Task]:
    """
    Args:
        task_id (str):
        json_body (PatchedTask):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Task]
    """

    kwargs = _get_kwargs(
        task_id=task_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    task_id: str,
    *,
    client: AuthenticatedClient,
    json_body: PatchedTask,
) -> Optional[Task]:
    """
    Args:
        task_id (str):
        json_body (PatchedTask):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Task
    """

    return sync_detailed(
        task_id=task_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    task_id: str,
    *,
    client: AuthenticatedClient,
    json_body: PatchedTask,
) -> Response[Task]:
    """
    Args:
        task_id (str):
        json_body (PatchedTask):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Task]
    """

    kwargs = _get_kwargs(
        task_id=task_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    task_id: str,
    *,
    client: AuthenticatedClient,
    json_body: PatchedTask,
) -> Optional[Task]:
    """
    Args:
        task_id (str):
        json_body (PatchedTask):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Task
    """

    return (
        await asyncio_detailed(
            task_id=task_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
