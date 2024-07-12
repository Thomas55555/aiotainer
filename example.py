"""An example file to use this library."""

import asyncio
import datetime
import logging
import time
from pprint import pprint
from typing import cast

import yaml
from aiohttp import ClientSession

from aiotainer.auth import AbstractAuth
from aiotainer.const import API_BASE_URL
from aiotainer.client import PortainerClient
from aiotainer.model import MowerData

_LOGGER = logging.getLogger(__name__)


# Fill out the secrets in secrets.yaml, you can find an example
# _secrets.yaml file, which has to be renamed after filling out the secrets.

with open("./secrets.yaml", encoding="UTF-8") as file:
    secrets = yaml.safe_load(file)

ACCESS_TOKEN = secrets["ACCESS_TOKEN"]


class AsyncTokenAuth(AbstractAuth):
    """Provide Automower authentication tied to an OAuth2 based config entry."""

    def __init__(
        self,
        websession: ClientSession,
    ) -> None:
        """Initialize Husqvarna Automower auth."""
        super().__init__(websession, API_BASE_URL)

    async def async_get_access_token(self) -> str:
        """Return a valid access token."""
        return ACCESS_TOKEN


async def main() -> None:
    """Establish connection to mower and print states for 5 minutes."""
    websession = ClientSession()
    automower_api = PortainerClient(AsyncTokenAuth(websession), poll=True)
    await asyncio.sleep(1)
    await automower_api.connect()
    for env_id in automower_api.data:
        test: MowerData = automower_api.data[env_id]
        for snapshot in test.snapshots:
            for container in snapshot.docker_snapshot_raw.containers:
                print(container.names[0].strip("/"), container.state, container.id)
                #await automower_api.start_container(env_id, container.id)
   # The close() will stop the websocket and the token refresh tasks
    await automower_api.close()
    await websession.close()



asyncio.run(main())
