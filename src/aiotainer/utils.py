"""Utils for Husqvarna Automower."""

import logging
from typing import Any

from .model import NodeData

_LOGGER = logging.getLogger(__name__)


def mower_list_to_dictionary_dataclass(
    mower_list: list[Any],
) -> dict[int, NodeData]:
    """Convert mower data to a dictionary DataClass."""
    _LOGGER.debug("mower_list: %s", mower_list)
    mowers_dict = {}
    for mower in mower_list:
        test = NodeData.from_dict(mower)
        mowers_dict[test.id] = test
    return mowers_dict
