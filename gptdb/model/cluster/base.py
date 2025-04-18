from typing import Any, Dict, List, Optional, Union

from gptdb._private.pydantic import BaseModel, Field
from gptdb.core.interface.message import ModelMessage
from gptdb.model.base import WorkerApplyType
from gptdb.model.parameter import WorkerType

WORKER_MANAGER_SERVICE_TYPE = "service"
WORKER_MANAGER_SERVICE_NAME = "WorkerManager"


class PromptRequest(BaseModel):
    model: str
    messages: List[ModelMessage] = Field(
        default_factory=list, description="List of ModelMessage objects"
    )
    prompt: str = None
    temperature: float = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    max_new_tokens: int = None
    stop: Optional[Union[str, List[str]]] = None
    stop_token_ids: List[int] = []
    context_len: int = None
    echo: bool = True
    span_id: str = None
    metrics: bool = False
    """Whether to return metrics of inference"""
    version: str = "v2"
    """Message version, default to v2"""
    context: Dict[str, Any] = None
    """Context information for the model"""
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    chat_model: Optional[bool] = True
    """Whether to use chat model"""


class EmbeddingsRequest(BaseModel):
    model: str
    input: List[str]
    span_id: Optional[str] = None
    query: Optional[str] = None
    """For rerank model, query is required"""


class CountTokenRequest(BaseModel):
    model: str
    prompt: str


class ModelMetadataRequest(BaseModel):
    model: str


class WorkerApplyRequest(BaseModel):
    model: str
    apply_type: WorkerApplyType
    worker_type: WorkerType = WorkerType.LLM
    params: Dict = None
    apply_user: str = None


class WorkerParameterRequest(BaseModel):
    model: str
    worker_type: WorkerType = WorkerType.LLM


class WorkerStartupRequest(BaseModel):
    host: str
    port: int
    model: str
    worker_type: WorkerType
    params: Dict
