from typing import Optional

from fastapi import APIRouter, Header
from fastapi import Body
from fastapi import Depends
from fastapi import Path
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from opencopilot.logger import api_logger
from opencopilot.authorization import validate_api_key_use_case
from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)
from opencopilot.repository.conversation_logs_repository import (
    ConversationLogsRepositoryLocal,
)
from opencopilot.repository.conversation_user_context_repository import (
    ConversationUserContextRepositoryLocal,
)
from opencopilot.repository.documents import document_store
from opencopilot.routers import routing_utils
from opencopilot.service import utils
from opencopilot.service.chat import chat_context_service, chat_service
from opencopilot.service.chat import (
    chat_feedback_service,
    chat_streaming_service,
    chat_history_service,
)
from opencopilot.service.chat.entities import ChatContextRequest
from opencopilot.service.chat.entities import ChatFeedbackRequest
from opencopilot.service.chat.entities import ChatHistoryRequest, ChatHistoryResponse
from opencopilot.service.chat.entities import ChatRequest
from opencopilot.service.chat.entities import ChatResponse
from opencopilot.service.entities import ApiResponse

TAG = "Chat"
router = APIRouter()
router.openapi_tags = [TAG]
router.title = "Chat router"

logger = api_logger.get()

STREAM_RESPONSE_DESCRIPTION = """
A stream of objects, delimited by newlines. Each object will be of the following form:
```
{
    "text": "some text" # the next chunk of the message from the copilot
    "error": ""         # if present, a string description of the error that occurred
}
```

For example, the message "I like to eat apples" might be streamed as follows:

```
{"text": "I like"}
{"text": " to eat"}
{"text": " apples"}
```
"""

CONVERSATION_ID_DESCRIPTION = """
The ID of the conversation. To start a new conversation, you should pass in a random uuid version 4 (Python: `import uuid; uuid.uuid4()`). To continue a conversation, re-use the same uuid.
"""


class ConversationInput(BaseModel):
    message: str = Field(
        ...,
        description="Message to be answered by the copilot.",
        example="How do I make a delicious lemon cheesecake?",
    )

    class Config:
        schema_extra = {
            "example": {
                "message": "How do I make a delicious lemon cheesecake?",
            }
        }


@router.get(
    "/conversations",
    summary="List conversations.",
    tags=[TAG],
)
async def handle_get_conversation_history(
    
):
    email: Optional[str] = Header(default=None),
    return None


@router.post(
    "/conversations/{conversation_id}",
    summary="Send a message to the copilot.",
    tags=[TAG],
)
async def handle_conversation(
    email: Optional[str] = Header(default=None),
    conversation_id: str = Path(
        ...,
        description=CONVERSATION_ID_DESCRIPTION,
    ),
    payload: ConversationInput = Body(
        ..., description="Input and parameters for the conversation."
    ),
    user_id: str = Depends(validate_api_key_use_case.execute),
):
    request = ChatRequest(
        chat_id=conversation_id,
        message=payload.inputs,
        response_message_id=payload.response_message_id,
        email=user_id or email,
    )

    history_repository = ConversationHistoryRepositoryLocal()
    logs_repository = ConversationLogsRepositoryLocal()

    response: ChatResponse = await chat_service.execute(
        request,
        document_store.get_document_store(),
        history_repository,
        logs_repository,
    )
    return routing_utils.to_json_response(
        {"generated_text": response.message, "sources": response.sources}
    )


@router.post(
    "/conversations/{conversation_id}/stream",
    summary="Send a message to the copilot and get the response as a stream.",
    response_description=STREAM_RESPONSE_DESCRIPTION,
    tags=[TAG],
)
async def handle_conversation_streaming(
    email: Optional[str] = Header(default=None),
    conversation_id: str = Path(..., description=CONVERSATION_ID_DESCRIPTION),
    payload: ConversationInput = Body(
        ..., description="Input and parameters for the conversation."
    ),
    user_id: str = Depends(validate_api_key_use_case.execute),
):
    request = ChatRequest(
        chat_id=conversation_id,
        message=payload.inputs,
        response_message_id=payload.response_message_id,
        email=user_id or email,
    )

    history_repository = ConversationHistoryRepositoryLocal()
    logs_repository = ConversationLogsRepositoryLocal()

    headers = {
        "X-Content-Type-Options": "nosniff",
        "Connection": "keep-alive",
    }
    return StreamingResponse(
        chat_streaming_service.execute(
            request,
            document_store.get_document_store(),
            history_repository,
            logs_repository,
        ),
        headers=headers,
        media_type="text/event-stream",
    )


@router.get(
    "/conversations/{conversation_id}",
    summary="Retrieve a conversation, including all message history within.",
    tags=[TAG],
)
async def handle_get_conversation_history(
    conversation_id: str = Path(..., description="The ID of the conversation."),
):
    request = ChatHistoryRequest(
        chat_id=conversation_id,
    )

    history_repository = ConversationHistoryRepositoryLocal()

    response: ChatHistoryResponse = await chat_history_service.execute(
        request,
        history_repository,
    )
    return response
