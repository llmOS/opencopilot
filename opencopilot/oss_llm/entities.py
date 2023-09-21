from typing import List

import pydantic
from pydantic import BaseModel
from pydantic import Field


class GenerateStreamRequest(BaseModel):
    query: str
    temperature: float = 0.1
    max_tokens: int


class TokenizeRequest(BaseModel):
    text: str


class TokenizeResponse(BaseModel):
    tokens: List[int] = Field(description="List of tokens")

    if pydantic.__version__.startswith("2"):
        model_config = {
            "json_schema_extra": {"example": {"tokens": [1, 52, 332, 44, 16]}}
        }
