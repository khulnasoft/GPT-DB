"""DBSchema retriever."""

from functools import reduce
from typing import List, Optional, cast

from gptdb.core import Chunk
from gptdb.datasource.base import BaseConnector
from gptdb.rag.index.base import IndexStoreBase
from gptdb.rag.retriever.base import BaseRetriever
from gptdb.rag.retriever.rerank import DefaultRanker, Ranker
from gptdb.rag.summary.rdbms_db_summary import _parse_db_summary
from gptdb.storage.vector_store.filters import MetadataFilters
from gptdb.util.chat_util import run_async_tasks
from gptdb.util.executor_utils import blocking_func_to_async_no_executor
from gptdb.util.tracer import root_tracer


class DBSchemaRetriever(BaseRetriever):
    """DBSchema retriever."""

    def __init__(
        self,
        index_store: IndexStoreBase,
        top_k: int = 4,
        connector: Optional[BaseConnector] = None,
        query_rewrite: bool = False,
        rerank: Optional[Ranker] = None,
        **kwargs
    ):
        """Create DBSchemaRetriever.

        Args:
            index_store(IndexStore): index connector
            top_k (int): top k
            connector (Optional[BaseConnector]): RDBMSConnector.
            query_rewrite (bool): query rewrite
            rerank (Ranker): rerank

        Examples:
            .. code-block:: python

                from gptdb.datasource.rdbms.conn_sqlite import SQLiteTempConnector
                from gptdb.serve.rag.assembler.db_schema import DBSchemaAssembler
                from gptdb.storage.vector_store.connector import VectorStoreConnector
                from gptdb.storage.vector_store.chroma_store import ChromaVectorConfig
                from gptdb.rag.retriever.embedding import EmbeddingRetriever


                def _create_temporary_connection():
                    connect = SQLiteTempConnector.create_temporary_db()
                    connect.create_temp_tables(
                        {
                            "user": {
                                "columns": {
                                    "id": "INTEGER PRIMARY KEY",
                                    "name": "TEXT",
                                    "age": "INTEGER",
                                },
                                "data": [
                                    (1, "Tom", 10),
                                    (2, "Jerry", 16),
                                    (3, "Jack", 18),
                                    (4, "Alice", 20),
                                    (5, "Bob", 22),
                                ],
                            }
                        }
                    )
                    return connect


                connector = _create_temporary_connection()
                embedding_fn = embedding_factory.create(model_name=embedding_model_path)
                config = ChromaVectorConfig(
                    persist_path=PILOT_PATH,
                    name="dbschema_rag_test",
                    embedding_fn=DefaultEmbeddingFactory(
                        default_model_name=os.path.join(
                            MODEL_PATH, "text2vec-large-chinese"
                        ),
                    ).create(),
                )

                vector_store = ChromaStore(config)
                # get db struct retriever
                retriever = DBSchemaRetriever(
                    top_k=3,
                    index_store=vector_store,
                    connector=connector,
                )
                chunks = retriever.retrieve("show columns from table")
                result = [chunk.content for chunk in chunks]
                print(f"db struct rag example results:{result}")
        """
        self._top_k = top_k
        self._connector = connector
        self._query_rewrite = query_rewrite
        self._index_store = index_store
        self._need_embeddings = False
        if self._index_store:
            self._need_embeddings = True
        self._rerank = rerank or DefaultRanker(self._top_k)

    def _retrieve(
        self, query: str, filters: Optional[MetadataFilters] = None
    ) -> List[Chunk]:
        """Retrieve knowledge chunks.

        Args:
            query (str): query text
            filters: metadata filters.

        Returns:
            List[Chunk]: list of chunks
        """
        if self._need_embeddings:
            queries = [query]
            candidates = [
                self._index_store.similar_search(query, self._top_k, filters)
                for query in queries
            ]
            return cast(List[Chunk], reduce(lambda x, y: x + y, candidates))
        else:
            if not self._connector:
                raise RuntimeError("RDBMSConnector connection is required.")
            table_summaries = _parse_db_summary(self._connector)
            return [Chunk(content=table_summary) for table_summary in table_summaries]

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
            filters: metadata filters.

        Returns:
            List[Chunk]: list of chunks
        """
        return self._retrieve(query, filters)

    async def _aretrieve(
        self, query: str, filters: Optional[MetadataFilters] = None
    ) -> List[Chunk]:
        """Retrieve knowledge chunks.

        Args:
            query (str): query text
            filters: metadata filters.

        Returns:
            List[Chunk]: list of chunks
        """
        if self._need_embeddings:
            queries = [query]
            candidates = [
                self._similarity_search(
                    query, filters, root_tracer.get_current_span_id()
                )
                for query in queries
            ]
            result_candidates = await run_async_tasks(
                tasks=candidates, concurrency_limit=1
            )
            return cast(List[Chunk], reduce(lambda x, y: x + y, result_candidates))
        else:
            from gptdb.rag.summary.rdbms_db_summary import (  # noqa: F401
                _parse_db_summary,
            )

            table_summaries = await run_async_tasks(
                tasks=[self._aparse_db_summary(root_tracer.get_current_span_id())],
                concurrency_limit=1,
            )
            return [
                Chunk(content=table_summary) for table_summary in table_summaries[0]
            ]

    async def _aretrieve_with_score(
        self,
        query: str,
        score_threshold: float,
        filters: Optional[MetadataFilters] = None,
    ) -> List[Chunk]:
        """Retrieve knowledge chunks with score.

        Args:
            query (str): query text
            score_threshold (float): score threshold
            filters: metadata filters.
        """
        return await self._aretrieve(query, filters)

    async def _similarity_search(
        self,
        query,
        filters: Optional[MetadataFilters] = None,
        parent_span_id: Optional[str] = None,
    ) -> List[Chunk]:
        """Similar search."""
        with root_tracer.start_span(
            "gptdb.rag.retriever.db_schema._similarity_search",
            parent_span_id,
            metadata={"query": query},
        ):
            return await blocking_func_to_async_no_executor(
                self._index_store.similar_search, query, self._top_k, filters
            )

    async def _aparse_db_summary(
        self, parent_span_id: Optional[str] = None
    ) -> List[str]:
        """Similar search."""
        from gptdb.rag.summary.rdbms_db_summary import _parse_db_summary

        if not self._connector:
            raise RuntimeError("RDBMSConnector connection is required.")
        with root_tracer.start_span(
            "gptdb.rag.retriever.db_schema._aparse_db_summary",
            parent_span_id,
        ):
            return await blocking_func_to_async_no_executor(
                _parse_db_summary, self._connector
            )
