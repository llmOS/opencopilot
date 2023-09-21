import pydantic
from pydantic import BaseModel
from pydantic import Field


class ApiResponse(BaseModel):
    response: str = Field(description="Response status, either OK or NOK.")

    if pydantic.__version__.startswith("2"):
        model_config = {"json_schema_extra": {"example": {"response": "OK"}}}
