"""Module to connect to Automower with websocket."""

import asyncio
import contextlib
import logging
from dataclasses import dataclass
from typing import Any, Iterable

from .auth import AbstractAuth
from .const import REST_POLL_CYCLE
from .model import NodeData
from .utils import mower_list_to_dictionary_dataclass

_LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)


@dataclass
class PortainerEndpoint:
    """Endpoint URLs for the Portainer API."""

    endpoints = "endpoints"
    "List data for all mowers linked to a user."

    endpoints_env = "endpoints/{env_id}"
    "List data for all mowers linked to a user."

    restart = "endpoints/{env_id}/docker/containers/{container_id}/restart"
    "Restart a specific container in an environment."

    start = "endpoints/{env_id}/docker/containers/{container_id}/start"
    "Start a specific container in an environment."

    stop = "endpoints/{env_id}/docker/containers/{container_id}/stop"
    "Stop a specific container in an environment."


class PortainerClient:
    """API to communicate with an Portainer.

    The `PortainerClient` is the primary API service for this library. It supports
    operations like getting a status or sending commands.
    """

    def __init__(
        self,
        auth: AbstractAuth,
        poll: bool = False,
    ) -> None:
        """Create a client.

        :param class auth: The AbstractAuth class from aiotainer.auth.
        :param bool poll: Poll data with rest if True.
        """
        self._data: dict[str, Iterable[Any]] | None = {}
        self.auth = auth
        self.data: dict[int, NodeData] = {}
        self.loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        self.poll = poll
        self.rest_task: asyncio.Task | None = None

    async def connect(self) -> None:
        """Connect to the API.

        This method handles the login. Also a REST task will be started, which
        periodically polls the REST endpoint, when polling is set to true.
        """

        if self.poll:
            await self.get_status()
            self.rest_task = asyncio.create_task(self._rest_task())

    async def get_status(self) -> dict[int, NodeData]:
        """Get status of all endpoints."""
        mower_list = await self.auth.get_json(PortainerEndpoint.endpoints)
        self.data = mower_list_to_dictionary_dataclass(mower_list)
        return self.data

    async def get_status_specific(self, env_id: int) -> NodeData:
        """Get status of a specific endpoint."""
        mower_list = await self.auth.get_json_node(
            PortainerEndpoint.endpoints_env.format(env_id=env_id)
        )
        self.data[env_id] = NodeData.from_dict(mower_list)
        return self.data[env_id]

    async def restart_container(self, env_id: int, container_id: str):
        """Restart container."""
        url = PortainerEndpoint.restart.format(env_id=env_id, container_id=container_id)
        await self.auth.post(url)

    async def start_container(self, env_id: int, container_id: str):
        """Start container."""
        url = PortainerEndpoint.start.format(env_id=env_id, container_id=container_id)
        await self.auth.post(url)

    async def stop_container(self, env_id: int, container_id: str):
        """Stop container."""
        url = PortainerEndpoint.stop.format(env_id=env_id, container_id=container_id)
        await self.auth.post(url)

    async def _rest_task(self) -> None:
        """Poll data periodically via Rest."""
        while True:
            await self.get_status()
            await asyncio.sleep(REST_POLL_CYCLE)

    async def close(self) -> None:
        """Close the client."""
        if self.rest_task:
            if not self.rest_task.cancelled():
                self.rest_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await asyncio.gather(self.rest_task)
