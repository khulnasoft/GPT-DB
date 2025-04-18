from dataclasses import dataclass, field
from typing import Optional

from gptdb.serve.core import BaseServeConfig

APP_NAME = "libro"
SERVE_APP_NAME = "gptdb_serve_libro"
SERVE_APP_NAME_HUMP = "gptdb_serve_Libro"
SERVE_CONFIG_KEY_PREFIX = "gptdb.serve.libro."
SERVE_SERVICE_COMPONENT_NAME = f"{SERVE_APP_NAME}_service"
# Database table name
SERVER_APP_TABLE_NAME = "gptdb_serve_libro"


@dataclass
class ServeConfig(BaseServeConfig):
    """Parameters for the serve command"""

    # TODO: add your own parameters here
    api_keys: Optional[str] = field(
        default=None, metadata={"help": "API keys for the endpoint, if None, allow all"}
    )
