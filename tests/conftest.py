"""Test helpers for Husqvarna Automower."""

import json
from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest
from syrupy import SnapshotAssertion

from tests import load_fixture

from .syrupy import AutomowerSnapshotExtension


@pytest.fixture(name="snapshot")
def snapshot_assertion(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return snapshot assertion fixture with the Automower extension."""
    return snapshot.use_extension(AutomowerSnapshotExtension)


@pytest.fixture()
def mock_automower_client() -> Generator[AsyncMock, None, None]:
    """Mock a Auth Automower client."""
    with patch(
        "aiotainer.auth.AbstractAuth",
        autospec=True,
    ) as mock_client:
        client = mock_client.return_value
        client.get.return_value = json.loads(load_fixture("get.json"))
        yield client
