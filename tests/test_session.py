"""Test aiotainert client."""

from typing import TYPE_CHECKING
from unittest.mock import AsyncMock

from aiotainer.auth import AbstractAuth
from aiotainer.client import PortainerClient

CONTAINER_ID = "c7233734-b219-4287-a173-08e3643f89f0"
NODE_ID = 2


async def test_connect_disconnect(mock_aiotainer_client: AbstractAuth):
    """Test aiotainer client post commands."""
    aiotainer_api = PortainerClient(mock_aiotainer_client, poll=True)
    await aiotainer_api.connect()
    await aiotainer_api.close()
    if TYPE_CHECKING:
        assert aiotainer_api.rest_task is not None
    assert aiotainer_api.rest_task.cancelled()


async def test_post_commands(mock_aiotainer_client: AbstractAuth):
    """Test aiotainer client post commands."""
    aiotainer_api = PortainerClient(mock_aiotainer_client, poll=True)
    await aiotainer_api.connect()
    mocked_method = AsyncMock()
    setattr(mock_aiotainer_client, "post", mocked_method)
    await aiotainer_api.start_container(NODE_ID, CONTAINER_ID)
    mocked_method.assert_called_with(
        f"api/endpoints/{NODE_ID}/docker/containers/{CONTAINER_ID}/start",
    )
    await aiotainer_api.stop_container(NODE_ID, CONTAINER_ID)
    mocked_method.assert_called_with(
        f"api/endpoints/{NODE_ID}/docker/containers/{CONTAINER_ID}/stop",
    )
    await aiotainer_api.restart_container(NODE_ID, CONTAINER_ID)
    mocked_method.assert_called_with(
        f"api/endpoints/{NODE_ID}/docker/containers/{CONTAINER_ID}/restart",
    )
