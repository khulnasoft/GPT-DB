from typing import Any

from gptdb.serve.core.config import BaseServeConfig
from gptdb.serve.core.schemas import Result, add_exception_handler
from gptdb.serve.core.serve import BaseServe
from gptdb.serve.core.service import BaseService
from gptdb.util.executor_utils import BlockingFunction, DefaultExecutorFactory
from gptdb.util.executor_utils import blocking_func_to_async as _blocking_func_to_async

__ALL__ = [
    "Result",
    "add_exception_handler",
    "BaseServeConfig",
    "BaseService",
    "BaseServe",
]


async def blocking_func_to_async(
    system_app, func: BlockingFunction, *args, **kwargs
) -> Any:
    """Run a potentially blocking function within an executor."""
    executor = DefaultExecutorFactory.get_instance(system_app).create()
    return await _blocking_func_to_async(executor, func, *args, **kwargs)
