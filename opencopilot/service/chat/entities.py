from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from opencopilot.service.entities import ApiResponse


class ConversationsRequest(BaseModel):
    user_id: Optional[str] = None


class ConversationsResponse(ApiResponse):
    conversations: List[str]


class ChatRequest(BaseModel):
    conversation_id: str = Field(description="Conversation id")
    message: str
    user_id: Optional[str] = None


class ChatResponse(ApiResponse):
    conversation_id: str = Field(description="Conversation id")

    message: str = Field(description="Conversation output")

    sources: List[str] = Field(default_factory=list, description="Sources")

    class Config:
        schema_extra = {
            "example": {
                "response": "OK",
                "conversation_id": "e91042aa-d53a-41eb-8884-67aa4947982d",
                "message": "I will use the 'search' command to find the weather in San Francisco.",
            }
        }


class ChatHistoryRequest(BaseModel):
    conversation_id: str = Field(description="Chat id")
    user_id: Optional[str] = None


class ChatHistoryItem(BaseModel):
    content: str
    timestamp: int
    response_message_id: str


class ChatHistoryResponse(BaseModel):
    response: str
    conversation_id: str = Field(description="Chat id")
    messages: List[ChatHistoryItem] = Field(
        default_factory=list, description="Messages"
    )


class ChatDeleteRequest(BaseModel):
    conversation_id: str = Field(description="Chat id")
    user_id: Optional[str] = None


class ChatDeleteResponse(ApiResponse):
    pass
