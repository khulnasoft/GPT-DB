"""Proxy models."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gptdb.model.proxy.llms.chatgpt import OpenAILLMClient
    from gptdb.model.proxy.llms.claude import ClaudeLLMClient
    from gptdb.model.proxy.llms.deepseek import DeepseekLLMClient
    from gptdb.model.proxy.llms.gemini import GeminiLLMClient
    from gptdb.model.proxy.llms.gitee import GiteeLLMClient
    from gptdb.model.proxy.llms.moonshot import MoonshotLLMClient
    from gptdb.model.proxy.llms.ollama import OllamaLLMClient
    from gptdb.model.proxy.llms.siliconflow import SiliconFlowLLMClient
    from gptdb.model.proxy.llms.spark import SparkLLMClient
    from gptdb.model.proxy.llms.tongyi import TongyiLLMClient
    from gptdb.model.proxy.llms.wenxin import WenxinLLMClient
    from gptdb.model.proxy.llms.yi import YiLLMClient
    from gptdb.model.proxy.llms.zhipu import ZhipuLLMClient


def __lazy_import(name):
    module_path = {
        "OpenAILLMClient": "gptdb.model.proxy.llms.chatgpt",
        "ClaudeLLMClient": "gptdb.model.proxy.llms.claude",
        "GeminiLLMClient": "gptdb.model.proxy.llms.gemini",
        "SiliconFlowLLMClient": "gptdb.model.proxy.llms.siliconflow",
        "SparkLLMClient": "gptdb.model.proxy.llms.spark",
        "TongyiLLMClient": "gptdb.model.proxy.llms.tongyi",
        "WenxinLLMClient": "gptdb.model.proxy.llms.wenxin",
        "ZhipuLLMClient": "gptdb.model.proxy.llms.zhipu",
        "YiLLMClient": "gptdb.model.proxy.llms.yi",
        "MoonshotLLMClient": "gptdb.model.proxy.llms.moonshot",
        "OllamaLLMClient": "gptdb.model.proxy.llms.ollama",
        "DeepseekLLMClient": "gptdb.model.proxy.llms.deepseek",
        "GiteeLLMClient": "gptdb.model.proxy.llms.gitee",
    }

    if name in module_path:
        module = __import__(module_path[name], fromlist=[name])
        return getattr(module, name)
    else:
        raise AttributeError(f"module {__name__} has no attribute {name}")


def __getattr__(name):
    return __lazy_import(name)


__all__ = [
    "OpenAILLMClient",
    "ClaudeLLMClient",
    "GeminiLLMClient",
    "TongyiLLMClient",
    "ZhipuLLMClient",
    "WenxinLLMClient",
    "SiliconFlowLLMClient",
    "SparkLLMClient",
    "YiLLMClient",
    "MoonshotLLMClient",
    "OllamaLLMClient",
    "DeepseekLLMClient",
    "GiteeLLMClient",
]
