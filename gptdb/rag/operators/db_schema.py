"""The DBSchema Retriever Operator."""
import os
from typing import List, Optional

from gptdb.core import Chunk
from gptdb.core.interface.operators.retriever import RetrieverOperator
from gptdb.datasource.base import BaseConnector
from gptdb.serve.rag.connector import VectorStoreConnector

from ...storage.vector_store.base import VectorStoreConfig
from ..assembler.db_schema import DBSchemaAssembler
from ..chunk_manager import ChunkParameters
from ..retriever.db_schema import DBSchemaRetriever
from .assembler import AssemblerOperator


class DBSchemaRetrieverOperator(RetrieverOperator[str, List[Chunk]]):
    """The DBSchema Retriever Operator.

    Args:
        connector (BaseConnector): The connection.
        top_k (int, optional): The top k. Defaults to 4.
        vector_store_connector (VectorStoreConnector, optional): The vector store
        connector. Defaults to None.
    """

    def __init__(
        self,
        table_vector_store_connector: VectorStoreConnector,
        field_vector_store_connector: VectorStoreConnector,
        top_k: int = 4,
        connector: Optional[BaseConnector] = None,
        **kwargs
    ):
        """Create a new DBSchemaRetrieverOperator."""
        super().__init__(**kwargs)
        self._retriever = DBSchemaRetriever(
            top_k=top_k,
            connector=connector,
            table_vector_store_connector=table_vector_store_connector,
            field_vector_store_connector=field_vector_store_connector,
        )

    def retrieve(self, query: str) -> List[Chunk]:
        """Retrieve the table schemas.

        Args:
            query (str): The query.
        """
        return self._retriever.retrieve(query)


class DBSchemaAssemblerOperator(AssemblerOperator[BaseConnector, List[Chunk]]):
    """The DBSchema Assembler Operator."""

    def __init__(
        self,
        connector: BaseConnector,
        table_vector_store_connector: VectorStoreConnector,
        field_vector_store_connector: VectorStoreConnector = None,
        chunk_parameters: Optional[ChunkParameters] = None,
        **kwargs
    ):
        """Create a new DBSchemaAssemblerOperator.

        Args:
            connector (BaseConnector): The connection.
            vector_store_connector (VectorStoreConnector): The vector store connector.
            chunk_parameters (Optional[ChunkParameters], optional): The chunk
                parameters.
        """
        if not chunk_parameters:
            chunk_parameters = ChunkParameters(chunk_strategy="CHUNK_BY_SIZE")
        self._chunk_parameters = chunk_parameters
        self._table_vector_store_connector = table_vector_store_connector

        field_vector_store_config = VectorStoreConfig(
            name=table_vector_store_connector.vector_store_config.name + "_field"
        )
        self._field_vector_store_connector = (
            field_vector_store_connector
            or VectorStoreConnector.from_default(
                os.getenv("VECTOR_STORE_TYPE", "Chroma"),
                self._table_vector_store_connector.current_embeddings,
                vector_store_config=field_vector_store_config,
            )
        )
        self._connector = connector
        super().__init__(**kwargs)

    def assemble(self, dummy_value) -> List[Chunk]:
        """Persist the database schema.

        Args:
            dummy_value: Dummy value, not used.

        Returns:
            List[Chunk]: The chunks.
        """
        assembler = DBSchemaAssembler.load_from_connection(
            connector=self._connector,
            chunk_parameters=self._chunk_parameters,
            table_vector_store_connector=self._table_vector_store_connector,
            field_vector_store_connector=self._field_vector_store_connector,
        )
        assembler.persist()
        return assembler.get_chunks()
