from typing import List, Optional

from gptdb._private.config import Config
from gptdb.component import ComponentType
from gptdb.configs.model_config import EMBEDDING_MODEL_CONFIG
from gptdb.core import Chunk
from gptdb.model import DefaultLLMClient
from gptdb.model.cluster import WorkerManagerFactory
from gptdb.rag.embedding.embedding_factory import EmbeddingFactory
from gptdb.rag.retriever import EmbeddingRetriever, QueryRewrite, Ranker
from gptdb.rag.retriever.base import BaseRetriever
from gptdb.serve.rag.connector import VectorStoreConnector
from gptdb.serve.rag.models.models import KnowledgeSpaceDao
from gptdb.serve.rag.retriever.qa_retriever import QARetriever
from gptdb.serve.rag.retriever.retriever_chain import RetrieverChain
from gptdb.storage.vector_store.filters import MetadataFilters
from gptdb.util.executor_utils import ExecutorFactory, blocking_func_to_async

CFG = Config()


class KnowledgeSpaceRetriever(BaseRetriever):
    """Knowledge Space retriever."""

    def __init__(
        self,
        space_id: str = None,
        top_k: Optional[int] = 4,
        query_rewrite: Optional[QueryRewrite] = None,
        rerank: Optional[Ranker] = None,
        llm_model: Optional[str] = None,
    ):
        """
        Args:
            space_id (str): knowledge space name
            top_k (Optional[int]): top k
            query_rewrite: (Optional[QueryRewrite]) query rewrite
            rerank: (Optional[Ranker]) rerank
        """
        if space_id is None:
            raise ValueError("space_id is required")
        self._space_id = space_id
        self._top_k = top_k
        self._query_rewrite = query_rewrite
        self._rerank = rerank
        self._llm_model = llm_model
        embedding_factory = CFG.SYSTEM_APP.get_component(
            "embedding_factory", EmbeddingFactory
        )
        embedding_fn = embedding_factory.create(
            model_name=EMBEDDING_MODEL_CONFIG[CFG.EMBEDDING_MODEL]
        )
        from gptdb.storage.vector_store.base import VectorStoreConfig

        space_dao = KnowledgeSpaceDao()
        space = space_dao.get_one({"id": space_id})
        worker_manager = CFG.SYSTEM_APP.get_component(
            ComponentType.WORKER_MANAGER_FACTORY, WorkerManagerFactory
        ).create()
        llm_client = DefaultLLMClient(worker_manager=worker_manager)
        config = VectorStoreConfig(
            name=space.name,
            embedding_fn=embedding_fn,
            llm_client=llm_client,
            llm_model=self._llm_model,
        )

        self._vector_store_connector = VectorStoreConnector(
            vector_store_type=space.vector_type,
            vector_store_config=config,
        )
        self._executor = CFG.SYSTEM_APP.get_component(
            ComponentType.EXECUTOR_DEFAULT, ExecutorFactory
        ).create()

        self._retriever_chain = RetrieverChain(
            retrievers=[
                QARetriever(space_id=space_id, top_k=top_k, embedding_fn=embedding_fn),
                EmbeddingRetriever(
                    index_store=self._vector_store_connector.index_client,
                    top_k=top_k,
                    query_rewrite=self._query_rewrite,
                    rerank=self._rerank,
                ),
            ],
            executor=self._executor,
        )

    def _retrieve(
        self, query: str, filters: Optional[MetadataFilters] = None
    ) -> List[Chunk]:
        """Retrieve knowledge chunks.

        Args:
            query (str): query text.
            filters: (Optional[MetadataFilters]) metadata filters.

        Return:
            List[Chunk]: list of chunks
        """
        candidates = self._retriever_chain.retrieve(query=query, filters=filters)
        return candidates

    def _retrieve_with_score(
        self,
        query: str,
        score_threshold: float,
        filters: Optional[MetadataFilters] = None,
    ) -> List[Chunk]:
        """Retrieve knowledge chunks with score.

        Args:
            query (str): query text
            score_threshold (float): score threshold
            filters: (Optional[MetadataFilters]) metadata filters.

        Return:
            List[Chunk]: list of chunks with score
        """
        candidates_with_scores = self._retriever_chain.retrieve_with_scores(
            query, score_threshold, filters
        )
        return candidates_with_scores

    async def _aretrieve(
        self, query: str, filters: Optional[MetadataFilters] = None
    ) -> List[Chunk]:
        """Retrieve knowledge chunks.

        Args:
            query (str): query text.
            filters: (Optional[MetadataFilters]) metadata filters.

        Return:
            List[Chunk]: list of chunks
        """
        candidates = await blocking_func_to_async(
            self._executor, self._retrieve, query, filters
        )
        return candidates

    async def _aretrieve_with_score(
        self,
        query: str,
        score_threshold: float,
        filters: Optional[MetadataFilters] = None,
    ) -> List[Chunk]:
        """Retrieve knowledge chunks with score.

        Args:
            query (str): query text.
            score_threshold (float): score threshold.
            filters: (Optional[MetadataFilters]) metadata filters.

        Return:
            List[Chunk]: list of chunks with score.
        """
        return await self._retriever_chain.aretrieve_with_scores(
            query, score_threshold, filters
        )
