from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from gptdb.core import ModelRequest, ModelRequestContext
from gptdb.model.parameter import ProxyModelParameters
from gptdb.model.proxy.base import ProxyLLMClient
from gptdb.model.utils.token_utils import ProxyTokenizerWrapper

if TYPE_CHECKING:
    from gptdb.core.interface.message import BaseMessage, ModelMessage

logger = logging.getLogger(__name__)


class ProxyModel:
    def __init__(
        self,
        model_params: ProxyModelParameters,
        proxy_llm_client: Optional[ProxyLLMClient] = None,
    ) -> None:
        self._model_params = model_params
        self._tokenizer = ProxyTokenizerWrapper()
        self.proxy_llm_client = proxy_llm_client

    def get_params(self) -> ProxyModelParameters:
        return self._model_params

    def count_token(
        self,
        messages: Union[str, BaseMessage, ModelMessage, List[ModelMessage]],
        model_name: Optional[int] = None,
    ) -> int:
        """Count token of given messages

        Args:
            messages (Union[str, BaseMessage, ModelMessage, List[ModelMessage]]): messages to count token
            model_name (Optional[int], optional): model name. Defaults to None.

        Returns:
            int: token count, -1 if failed
        """
        return self._tokenizer.count_token(messages, model_name)


def parse_model_request(
    params: Dict[str, Any], default_model: str, stream: bool = True
) -> ModelRequest:
    """Parse model request from params.

    Args:
        params (Dict[str, Any]): request params
        default_model (str): default model name
        stream (bool, optional): whether stream. Defaults to True.
    """
    context = ModelRequestContext(
        stream=stream,
        user_name=params.get("user_name"),
        request_id=params.get("request_id"),
    )
    request = ModelRequest.build_request(
        default_model,
        messages=params["messages"],
        temperature=params.get("temperature"),
        context=context,
        max_new_tokens=params.get("max_new_tokens"),
        stop=params.get("stop"),
        top_p=params.get("top_p"),
    )
    return request
