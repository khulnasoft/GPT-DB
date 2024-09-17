"""OpenSPG class."""
import logging

from gptdb._private.pydantic import ConfigDict
from gptdb.storage.knowledge_graph.base import KnowledgeGraphBase, KnowledgeGraphConfig

logger = logging.getLogger(__name__)


class OpenSPGConfig(KnowledgeGraphConfig):
    """OpenSPG config."""

    model_config = ConfigDict(arbitrary_types_allowed=True)


class OpenSPG(KnowledgeGraphBase):
    """OpenSPG class."""

    # todo: add OpenSPG implementation
