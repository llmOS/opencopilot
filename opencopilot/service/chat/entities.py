from typing import List
from typing import Optional

import pydantic
from pydantic import BaseModel
from pydantic import Field

from opencopilot.service.entities import ApiResponse


class ConversationsRequest(BaseModel):
    user_id: Optional[str] = None


class ConversationsResponse(ApiResponse):
    conversation_ids: List[str]

    if pydantic.__version__.startswith("2"):
        model_config = {
            "json_schema_extra": {
                "example": {
                    "response": "OK",
                    "conversation_ids": ["e91042aa-d53a-41eb-8884-67aa4947982d"],
                }
            }
        }


class MessageHistoryItem(BaseModel):
    type: str
    message: str


class ConversationInput(BaseModel):
    message: str = Field(
        ...,
        description="Message to be answered by the copilot.",
        examples=["How do I make a delicious lemon cheesecake?"],
    )
    message_history: Optional[List[MessageHistoryItem]] = Field(
        default=[],
        description="Message history of the current conversation",
    )

    if pydantic.__version__.startswith("2"):
        model_config = {
            "json_schema_extra": {
                "example": {
                    "message": "How do I make a delicious lemon cheesecake?",
                }
            }
        }
    else:

        class Config:
            schema_extra = {
                "example": {
                    "message": "How do I make a delicious lemon cheesecake?",
                }
            }


class ChatRequest(BaseModel):
    conversation_id: str = Field(description="Conversation id")
    message: str
    message_history: Optional[List[MessageHistoryItem]]
    user_id: Optional[str] = None


class ChatResponse(ApiResponse):
    response_message_id: str = Field(
        description="Response message ID, useful for debugging"
    )
    copilot_message: str = Field(description="Conversation output")
    sources: List[str] = Field(default_factory=list, description="Sources")

    if pydantic.__version__.startswith("2"):
        model_config = {
            "json_schema_extra": {
                "example": {
                    "response": "OK",
                    "response_message_id": "d5c10659-ce34-4fdd-b5b0-cb20d110a5e9",
                    "copilot_message": "I will use the 'search' command to find the weather in San Francisco.",
                    "sources": [],
                }
            }
        }


class ChatHistoryRequest(BaseModel):
    conversation_id: str = Field(description="Chat id")
    user_id: Optional[str] = None


class ChatHistoryItem(BaseModel):
    content: str
    timestamp: float
    response_message_id: str


class ChatHistoryResponse(BaseModel):
    response: str
    conversation_id: str = Field(description="Chat id")
    messages: List[ChatHistoryItem] = Field(
        default_factory=list, description="Messages"
    )

    if pydantic.__version__.startswith("2"):
        model_config = {
            "json_schema_extra": {
                "example": {
                    "response": "OK",
                    "conversation_id": "e91042aa-d53a-41eb-8884-67aa4947982d",
                    "messages": [
                        {
                            "content": "Hello",
                            "timestamp": 1693562530,
                            "response_message_id": "ed02eedf-7a74-4a31-8fbf-eeb4300faf31",
                        },
                        {
                            "content": "Hello, how are you?",
                            "timestamp": 1693562539,
                            "response_message_id": "ed02eedf-7a74-4a31-8fbf-eeb4300faf31",
                        },
                    ],
                }
            }
        }


class ChatDeleteRequest(BaseModel):
    conversation_id: str = Field(description="Chat id")
    user_id: Optional[str] = None


class ChatDeleteResponse(ApiResponse):
    pass
