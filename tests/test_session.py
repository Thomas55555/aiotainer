"""Test automower client."""

import json
from datetime import timedelta
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock

import pytest
from aiohttp import WSMessage, WSMsgType

from aiotainer.auth import AbstractAuth
from aiotainer.exceptions import NoDataAvailableException
from aiotainer.model import NodeData
from aiotainer.client import PortainerClient
from tests import load_fixture

CONTAINER_ID = "c7233734-b219-4287-a173-08e3643f89f0"
NODE_ID = 2

async def test_connect_disconnect(mock_automower_client: AbstractAuth):
    """Test automower client post commands."""
    automower_api = PortainerClient(mock_automower_client, poll=True)
    await automower_api.connect()
    await automower_api.close()
    if TYPE_CHECKING:
        assert automower_api.rest_task is not None
    assert automower_api.rest_task.cancelled()


async def test_post_commands(mock_automower_client: AbstractAuth):
    """Test automower client post commands."""
    automower_api = PortainerClient(mock_automower_client, poll=True)
    await automower_api.connect()
    mocked_method = AsyncMock()
    setattr(mock_automower_client, "post", mocked_method)
    await automower_api.start_container(NODE_ID, CONTAINER_ID)
    mocked_method.assert_called_with(
        f"endpoints/{NODE_ID}/docker/containers/{CONTAINER_ID}/start",
    )
