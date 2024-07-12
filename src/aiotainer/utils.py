"""Utils for Husqvarna Automower."""

import logging
import time
from datetime import timedelta
from typing import Any, Mapping, cast
from urllib.parse import quote_plus, urlencode

import aiohttp



from .exceptions import ApiException
from .model import  NodeData

_LOGGER = logging.getLogger(__name__)



def mower_list_to_dictionary_dataclass(
    mower_list: Mapping[Any, Any],
) -> dict[str, NodeData]:
    """Convert mower data to a dictionary DataClass."""
    _LOGGER.debug("mower_list: %s",mower_list)
    mowers_dict = {}
    for mower in mower_list:
        _LOGGER.debug("mower: %s",mower)
        test=NodeData.from_dict(mower)
        _LOGGER.debug("test: %s",test)
        mowers_dict[test.id] = test
    return mowers_dict


