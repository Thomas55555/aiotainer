"""An example file to use this library."""

import asyncio
import logging
import pprint

import yaml
from aiohttp import ClientSession

from aiotainer.auth import AbstractAuth
from aiotainer.client import PortainerClient

_LOGGER = logging.getLogger(__name__)


# Fill out the secrets in secrets.yaml, you can find an example
# _secrets.yaml file, which has to be renamed after filling out the secrets.

with open("./secrets.yaml", encoding="UTF-8") as file:
    secrets = yaml.safe_load(file)

ACCESS_TOKEN = secrets["ACCESS_TOKEN"]
API_BASE_URL = secrets["API_BASE_URL"]


class AsyncTokenAuth(AbstractAuth):
    """Provide aiotainer authentication tied to an OAuth2 based config entry."""

    def __init__(
        self,
        websession: ClientSession,
    ) -> None:
        """Initialize aiotainer auth."""
        super().__init__(websession, API_BASE_URL)

    async def async_get_access_token(self) -> str:
        """Return a valid access token."""
        return ACCESS_TOKEN


async def main() -> None:
    """Establish connection to portainer and print states."""
    websession = ClientSession()
    aiotainer_api = PortainerClient(AsyncTokenAuth(websession), poll=True)
    await aiotainer_api.connect()
    for test in aiotainer_api.data.values():
        for snapshot in test.snapshots:
            for container in snapshot.docker_snapshot_raw.containers:
                print(container.names[0].strip("/"), container.state, container.id)
    a = await aiotainer_api.get_status_specific(2)
    pprint.pprint(a)
    await asyncio.sleep(2000)
    await aiotainer_api.close()
    await websession.close()


asyncio.run(main())
