from dataclasses import dataclass, field
from typing import Optional

from gptdb.serve.core import BaseServeConfig

APP_NAME = "{__template_app_name__all_lower__}"
SERVE_APP_NAME = "gptdb_serve_{__template_app_name__all_lower__}"
SERVE_APP_NAME_HUMP = "gptdb_serve_{__template_app_name__hump__}"
SERVE_CONFIG_KEY_PREFIX = "gptdb.serve.{__template_app_name__all_lower__}."
SERVE_SERVICE_COMPONENT_NAME = f"{SERVE_APP_NAME}_service"
# Database table name
SERVER_APP_TABLE_NAME = "gptdb_serve_{__template_app_name__all_lower__}"


@dataclass
class ServeConfig(BaseServeConfig):
    """Parameters for the serve command"""

    # TODO: add your own parameters here
    api_keys: Optional[str] = field(
        default=None, metadata={"help": "API keys for the endpoint, if None, allow all"}
    )
