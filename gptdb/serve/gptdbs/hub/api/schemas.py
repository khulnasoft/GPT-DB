# Define your Pydantic schemas here
from typing import Any, Dict, Optional

from gptdb._private.pydantic import BaseModel, ConfigDict, Field, model_to_dict

from ..config import SERVE_APP_NAME_HUMP


class ServeRequest(BaseModel):
    """GptdbsHub request model"""

    id: Optional[int] = Field(None, description="id")
    name: Optional[str] = Field(None, description="Gptdbs name")
    type: Optional[str] = Field(None, description="Gptdbs type")
    version: Optional[str] = Field(None, description="Gptdbs version")
    description: Optional[str] = Field(None, description="Gptdbs description")
    author: Optional[str] = Field(None, description="Gptdbs author")
    email: Optional[str] = Field(None, description="Gptdbs email")
    storage_channel: Optional[str] = Field(None, description="Gptdbs storage channel")
    storage_url: Optional[str] = Field(None, description="Gptdbs storage url")
    download_param: Optional[str] = Field(None, description="Gptdbs download param")
    installed: Optional[int] = Field(None, description="Gptdbs installed")

    model_config = ConfigDict(title=f"ServeRequest for {SERVE_APP_NAME_HUMP}")

    def to_dict(self, **kwargs) -> Dict[str, Any]:
        """Convert the model to a dictionary"""
        return model_to_dict(self, **kwargs)


class ServerResponse(ServeRequest):
    gmt_created: Optional[str] = Field(None, description="Gptdbs create time")
    gmt_modified: Optional[str] = Field(None, description="Gptdbs upload time")
