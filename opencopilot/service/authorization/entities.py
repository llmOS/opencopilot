import pydantic
from pydantic import BaseModel
from pydantic import Field

from opencopilot.service.entities import ApiResponse


class TokenRequest(BaseModel):
    client_id: str = Field(description="Client id")
    client_secret: str = Field(description="Client secret")
    user_id: str = Field(description="User id")


class TokenResponse(ApiResponse):
    token: str = Field(description="JWT token")

    if pydantic.__version__.startswith("2"):
        model_config = {
            "json_schema_extra": {
                "example": {
                    "response": "OK",
                    "token": "e91042aa-d53a-41eb-8884-67aa4947982d",
                }
            }
        }
