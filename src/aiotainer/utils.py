"""Utils for aiotainer."""

import logging
from typing import Any

from .model import NodeData

_LOGGER = logging.getLogger(__name__)


def portainer_list_to_dictionary(portainer_list):
    """Convert portainer data to a dictionary."""
    return {
        NodeData.from_dict(portainer).id: NodeData.from_dict(portainer)
        for portainer in portainer_list
    }
