"""Define the CommunityStore class."""

import logging
from typing import List

from gptdb.rag.transformer.community_summarizer import CommunitySummarizer
from gptdb.storage.knowledge_graph.community.base import (
    Community,
    CommunityStoreAdapter,
)
from gptdb.storage.knowledge_graph.community.community_metastore import (
    BuiltinCommunityMetastore,
)
from gptdb.storage.vector_store.base import VectorStoreBase

logger = logging.getLogger(__name__)


class CommunityStore:
    """CommunityStore Class."""

    def __init__(
        self,
        community_store_adapter: CommunityStoreAdapter,
        community_summarizer: CommunitySummarizer,
        vector_store: VectorStoreBase,
    ):
        """Initialize the CommunityStore class."""
        self._community_store_adapter = community_store_adapter
        self._community_summarizer = community_summarizer
        self._meta_store = BuiltinCommunityMetastore(vector_store)

    async def build_communities(self):
        """Discover communities."""
        community_ids = await self._community_store_adapter.discover_communities()

        # summarize communities
        communities = []
        for community_id in community_ids:
            community = await self._community_store_adapter.get_community(community_id)
            graph = community.data.format()
            if not graph:
                break

            community.summary = await self._community_summarizer.summarize(graph=graph)
            communities.append(community)
            logger.info(
                f"Summarize community {community_id}: " f"{community.summary[:50]}..."
            )

        # truncate then save new summaries
        await self._meta_store.truncate()
        await self._meta_store.save(communities)

    async def search_communities(self, query: str) -> List[Community]:
        """Search communities."""
        return await self._meta_store.search(query)

    def truncate(self):
        """Truncate community store."""
        logger.info("Truncate community metastore")
        self._meta_store.truncate()

        logger.info("Truncate community summarizer")
        self._community_summarizer.truncate()

        logger.info("Truncate graph")
        self._community_store_adapter.graph_store.truncate()

    def drop(self):
        """Drop community store."""
        logger.info("Remove community metastore")
        self._meta_store.drop()

        logger.info("Remove community summarizer")
        self._community_summarizer.drop()

        logger.info("Remove graph")
        self._community_store_adapter.graph_store.drop()