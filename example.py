"""An example file to use this library."""

import asyncio
import logging
import pprint

import yaml
from aiohttp import ClientSession

from aiotainer.auth import Auth
from aiotainer.client import PortainerClient

_LOGGER = logging.getLogger(__name__)


# Fill out the secrets in secrets.yaml, you can find an example
# _secrets.yaml file, which has to be renamed after filling out the secrets.

with open("./secrets.yaml", encoding="UTF-8") as file:
    secrets = yaml.safe_load(file)

ACCESS_TOKEN = secrets["ACCESS_TOKEN"]
HOST_URL = secrets["HOST_URL"]


async def main() -> None:
    """Establish connection to portainer and print states."""
    websession = ClientSession()
    auth = Auth(websession, HOST_URL, ACCESS_TOKEN)
    aiotainer_api = PortainerClient(auth, poll=True)
    await aiotainer_api.connect()
    settings = await aiotainer_api.get_settings()
    pprint.pprint(settings)
    for node in aiotainer_api.data:
        for container_id in (
            aiotainer_api.data[node].snapshots[-1].docker_snapshot_raw.containers
        ):
            pprint.pprint(
                aiotainer_api.data[node]
                .snapshots[-1]
                .docker_snapshot_raw.containers[container_id]
            )
    await asyncio.sleep(2000)
    await aiotainer_api.close()
    await websession.close()


asyncio.run(main())
