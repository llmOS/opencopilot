from typing import List
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field

from opencopilot.service.entities import ApiResponse


class ConversationsRequest(BaseModel):
    user_id: Optional[str] = None


class ConversationsResponse(ApiResponse):
    conversations: List[str]


class ChatRequest(BaseModel):
    chat_id: str = Field(description="Chat id")
    message: str
    response_message_id: Optional[str] = None
    user_id: Optional[str] = None


class ChatResponse(ApiResponse):
    chat_id: str = Field(description="Chat id")

    message: str = Field(description="Chat output")

    sources: List[str] = Field(default_factory=list, description="Sources")

    class Config:
        schema_extra = {
            "example": {
                "response": "OK",
                "chat_id": "e91042aa-d53a-41eb-8884-67aa4947982d",
                "message": "I will use the 'search' command to find the weather in San Francisco.",
            }
        }


class ChatFeedbackRequest(BaseModel):
    correctness: int = Field(
        description="How correct was the answer", ge=1, le=5, default=None
    )
    helpfulness: int = Field(
        description="How helpful was the answer", ge=1, le=5, default=None
    )
    easy_to_understand: int = Field(
        description="How easy to understand was the answer", ge=1, le=5, default=None
    )
    free_form_feedback: Optional[str] = Field(
        description="Free form user feedback for the answer"
    )


class CustomChatRequest(BaseModel):
    chat_id: str = Field(description="Chat id")
    copilot_id: str = Field(description="Copilot id")
    message: str
    response_message_id: Optional[str] = None


class ChatHistoryRequest(BaseModel):
    chat_id: str = Field(description="Chat id")
    user_id: Optional[str] = None


class ChatHistoryItem(BaseModel):
    content: str
    timestamp: int


class ChatHistoryResponse(BaseModel):
    response: str
    chat_id: str = Field(description="Chat id")
    messages: List[ChatHistoryItem] = Field(
        default_factory=list, description="Messages"
    )


class ChatContextRequest(BaseModel):
    context: str = Field(description="Additional context relevant to conversation")


class ChatDeleteRequest(BaseModel):
    conversation_id: str = Field(description="Chat id")
    user_id: Optional[str] = None


class ChatDeleteResponse(ApiResponse):
    pass
