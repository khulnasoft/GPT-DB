from __future__ import annotations

import logging
from typing import List, Optional, Type, cast

from gptdb.configs.model_config import get_device
from gptdb.core import Embeddings, RerankEmbeddings
from gptdb.model.parameter import (
    BaseEmbeddingModelParameters,
    EmbeddingModelParameters,
    ProxyEmbeddingParameters,
)
from gptdb.util.parameter_utils import EnvArgumentParser, _get_dict_from_obj
from gptdb.util.system_utils import get_system_info
from gptdb.util.tracer import SpanType, SpanTypeRunName, root_tracer

logger = logging.getLogger(__name__)


class EmbeddingLoader:
    def __init__(self) -> None:
        pass

    def load(self, model_name: str, param: BaseEmbeddingModelParameters) -> Embeddings:
        metadata = {
            "model_name": model_name,
            "run_service": SpanTypeRunName.EMBEDDING_MODEL.value,
            "params": _get_dict_from_obj(param),
            "sys_infos": _get_dict_from_obj(get_system_info()),
        }
        with root_tracer.start_span(
            "EmbeddingLoader.load", span_type=SpanType.RUN, metadata=metadata
        ):
            # add more models
            if model_name in ["proxy_openai", "proxy_azure"]:
                from langchain.embeddings import OpenAIEmbeddings

                from gptdb.rag.embedding._wrapped import WrappedEmbeddings

                return WrappedEmbeddings(OpenAIEmbeddings(**param.build_kwargs()))
            elif model_name in ["proxy_http_openapi"]:
                from gptdb.rag.embedding import OpenAPIEmbeddings

                proxy_param = cast(ProxyEmbeddingParameters, param)
                openapi_param = {}
                if proxy_param.proxy_server_url:
                    openapi_param["api_url"] = proxy_param.proxy_server_url
                if proxy_param.proxy_api_key:
                    openapi_param["api_key"] = proxy_param.proxy_api_key
                if proxy_param.proxy_backend:
                    openapi_param["model_name"] = proxy_param.proxy_backend
                return OpenAPIEmbeddings(**openapi_param)
            elif model_name in ["proxy_tongyi"]:
                from gptdb.rag.embedding import TongYiEmbeddings

                proxy_param = cast(ProxyEmbeddingParameters, param)
                tongyi_param = {"api_key": proxy_param.proxy_api_key}
                if proxy_param.proxy_backend:
                    tongyi_param["model_name"] = proxy_param.proxy_backend
                return TongYiEmbeddings(**tongyi_param)
            elif model_name in ["proxy_qianfan"]:
                from gptdb.rag.embedding import QianFanEmbeddings

                proxy_param = cast(ProxyEmbeddingParameters, param)
                qianfan_param = {"api_key": proxy_param.proxy_api_key}
                if proxy_param.proxy_backend:
                    qianfan_param["model_name"] = proxy_param.proxy_backend
                    qianfan_param["api_secret"] = proxy_param.proxy_api_secret
                return QianFanEmbeddings(**qianfan_param)
            elif model_name in ["proxy_ollama"]:
                from gptdb.rag.embedding import OllamaEmbeddings

                proxy_param = cast(ProxyEmbeddingParameters, param)
                ollama_param = {}
                if proxy_param.proxy_server_url:
                    ollama_param["api_url"] = proxy_param.proxy_server_url
                if proxy_param.proxy_backend:
                    ollama_param["model_name"] = proxy_param.proxy_backend
                return OllamaEmbeddings(**ollama_param)
            else:
                from gptdb.rag.embedding import HuggingFaceEmbeddings

                kwargs = param.build_kwargs(model_name=param.model_path)
                return HuggingFaceEmbeddings(**kwargs)

    def load_rerank_model(
        self, model_name: str, param: BaseEmbeddingModelParameters
    ) -> RerankEmbeddings:
        metadata = {
            "model_name": model_name,
            "run_service": SpanTypeRunName.EMBEDDING_MODEL.value,
            "params": _get_dict_from_obj(param),
            "sys_infos": _get_dict_from_obj(get_system_info()),
        }
        with root_tracer.start_span(
            "EmbeddingLoader.load_rerank_model",
            span_type=SpanType.RUN,
            metadata=metadata,
        ):
            if model_name in ["rerank_proxy_http_openapi"]:
                from gptdb.rag.embedding.rerank import OpenAPIRerankEmbeddings

                proxy_param = cast(ProxyEmbeddingParameters, param)
                openapi_param = {}
                if proxy_param.proxy_server_url:
                    openapi_param["api_url"] = proxy_param.proxy_server_url
                if proxy_param.proxy_api_key:
                    openapi_param["api_key"] = proxy_param.proxy_api_key
                if proxy_param.proxy_backend:
                    openapi_param["model_name"] = proxy_param.proxy_backend
                return OpenAPIRerankEmbeddings(**openapi_param)
            elif model_name in ["rerank_proxy_siliconflow"]:
                from gptdb.rag.embedding.rerank import SiliconFlowRerankEmbeddings

                proxy_param = cast(ProxyEmbeddingParameters, param)
                openapi_param = {}
                if proxy_param.proxy_server_url:
                    openapi_param["api_url"] = proxy_param.proxy_server_url
                if proxy_param.proxy_api_key:
                    openapi_param["api_key"] = proxy_param.proxy_api_key
                if proxy_param.proxy_backend:
                    openapi_param["model_name"] = proxy_param.proxy_backend
                return SiliconFlowRerankEmbeddings(**openapi_param)
            else:
                from gptdb.rag.embedding.rerank import CrossEncoderRerankEmbeddings

                kwargs = param.build_kwargs(model_name=param.model_path)
                return CrossEncoderRerankEmbeddings(**kwargs)


def _parse_embedding_params(
    model_name: Optional[str] = None,
    model_path: Optional[str] = None,
    command_args: List[str] = None,
    param_cls: Optional[Type] = EmbeddingModelParameters,
    **kwargs,
):
    model_args = EnvArgumentParser()
    env_prefix = EnvArgumentParser.get_env_prefix(model_name)
    model_params: BaseEmbeddingModelParameters = model_args.parse_args_into_dataclass(
        param_cls,
        env_prefixes=[env_prefix],
        command_args=command_args,
        model_name=model_name,
        model_path=model_path,
        **kwargs,
    )
    if not model_params.device:
        model_params.device = get_device()
        logger.info(
            f"[EmbeddingsModelWorker] Parameters of device is None, use {model_params.device}"
        )
    return model_params
