"""Test helpers for aiotainer."""

import json
from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest
from syrupy import SnapshotAssertion

from tests import load_fixture

from .syrupy import AiotainerSnapshotExtension


@pytest.fixture(name="snapshot")
def snapshot_assertion(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return snapshot assertion fixture with the Aiotainer extension."""
    return snapshot.use_extension(AiotainerSnapshotExtension)


@pytest.fixture
def mock_aiotainer_client() -> Generator[AsyncMock, None, None]:
    """Mock a Auth aiotainer client."""
    with patch(
        "aiotainer.auth.Auth",
        autospec=True,
    ) as mock_client:
        client = mock_client.return_value
        client.get.return_value = json.loads(load_fixture("get.json"))
        yield client
