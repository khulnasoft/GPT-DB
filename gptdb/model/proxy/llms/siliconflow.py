import os
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from gptdb.model.proxy.llms.proxy_model import ProxyModel, parse_model_request

from .chatgpt import OpenAILLMClient

if TYPE_CHECKING:
    from httpx._types import ProxiesTypes
    from openai import AsyncAzureOpenAI, AsyncOpenAI

    ClientType = Union[AsyncAzureOpenAI, AsyncOpenAI]


_SILICONFLOW_DEFAULT_MODEL = "Qwen/Qwen2.5-Coder-32B-Instruct"


async def siliconflow_generate_stream(
    model: ProxyModel, tokenizer, params, device, context_len=2048
):
    client: SiliconFlowLLMClient = model.proxy_llm_client
    request = parse_model_request(params, client.default_model, stream=True)
    async for r in client.generate_stream(request):
        yield r


class SiliconFlowLLMClient(OpenAILLMClient):
    """SiliconFlow LLM Client.

    SiliconFlow's API is compatible with OpenAI's API, so we inherit from OpenAILLMClient.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        api_type: Optional[str] = None,
        api_version: Optional[str] = None,
        model: Optional[str] = None,
        proxies: Optional["ProxiesTypes"] = None,
        timeout: Optional[int] = 240,
        model_alias: Optional[str] = "siliconflow_proxyllm",
        context_length: Optional[int] = None,
        openai_client: Optional["ClientType"] = None,
        openai_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        api_base = (
            api_base
            or os.getenv("SILICONFLOW_API_BASE")
            or "https://api.siliconflow.cn/v1"
        )
        api_key = api_key or os.getenv("SILICONFLOW_API_KEY")
        model = model or _SILICONFLOW_DEFAULT_MODEL
        if not context_length:
            if "200k" in model:
                context_length = 200 * 1024
            else:
                context_length = 4096

        if not api_key:
            raise ValueError(
                "SiliconFlow API key is required, please set 'SILICONFLOW_API_KEY' in environment "
                "or pass it as an argument."
            )

        super().__init__(
            api_key=api_key,
            api_base=api_base,
            api_type=api_type,
            api_version=api_version,
            model=model,
            proxies=proxies,
            timeout=timeout,
            model_alias=model_alias,
            context_length=context_length,
            openai_client=openai_client,
            openai_kwargs=openai_kwargs,
            **kwargs
        )

    @property
    def default_model(self) -> str:
        model = self._model
        if not model:
            model = _SILICONFLOW_DEFAULT_MODEL
        return model
