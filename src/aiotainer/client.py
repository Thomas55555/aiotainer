"""Module to connect to Automower with websocket."""

import asyncio
import contextlib
import datetime
import logging
from dataclasses import dataclass
from typing import Any, Iterable, Literal, Mapping

from aiohttp import WSMessage, WSMsgType

from .auth import AbstractAuth
from .const import EVENT_TYPES, REST_POLL_CYCLE
from .exceptions import NoDataAvailableException, TimeoutException
from .model import NodeData
from .utils import mower_list_to_dictionary_dataclass

_LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)


@dataclass
class PortainerEndpoint:
    """Endpoint URLs for the AutomowerConnect API."""

    entpoints = "endpoints"
    "List data for all mowers linked to a user."

    start = "endpoints/{env_id}/docker/containers/{container_id}/start"
    "List data for all mowers linked to a user."

class PortainerClient:
    """Automower API to communicate with an Automower.

    The `AutomowerSession` is the primary API service for this library. It supports
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
        self.pong_cbs: list = []
        self.data_update_cbs: list = []
        self.data: dict[str, MowerAttributes] = {}
        self.last_ws_message: datetime.datetime
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


    async def get_status(self) -> None:
        """Get mower status via Rest."""
        mower_list = await self.auth.get_json(PortainerEndpoint.entpoints)
        self._data = mower_list
        self.data = mower_list_to_dictionary_dataclass(self._data)
        return self.data

    # def _update_data(self, new_data) -> None:
    #     """Update internal data, with new data from websocket."""
    #     if self._data is None:
    #         raise NoDataAvailableException

    #     data = self._data["data"]
    #     for mower in data:
    #         if mower["type"] == "mower" and mower["id"] == new_data["id"]:
    #             new_attributes: Mapping[Any, Any] = new_data["attributes"]
    #             value: Mapping[Any, Any]
    #             for attrib, value in new_attributes.items():
    #                 mower["attributes"][attrib] = value
    #     self.data = mower_list_to_dictionary_dataclass(self._data)
    #     self._schedule_data_callbacks()

    async def start_container(self, env_id: int, container_id: str):
        """Resume schedule.

        Remove any override on the Planner and let the mower
        resume to the schedule set by the Calendar.
        """
        #body = {}
        url = PortainerEndpoint.start.format(env_id=env_id, container_id=container_id)
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
