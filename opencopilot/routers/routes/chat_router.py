from typing import Optional

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Body
from fastapi import Depends
from fastapi import Request
from fastapi import Path
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pydantic import Field

from opencopilot.analytics import track
from opencopilot.analytics import TrackingEventType
from opencopilot.authorization import validate_api_key_use_case
from opencopilot.logger import api_logger
from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)
from opencopilot.repository.conversation_logs_repository import (
    ConversationLogsRepositoryLocal,
)
from opencopilot.repository.documents import document_store
from opencopilot.repository.users_repository import UsersRepositoryLocal
from opencopilot.service.chat import chat_conversations_service
from opencopilot.service.chat import chat_delete_service
from opencopilot.service.chat import chat_history_service
from opencopilot.service.chat import chat_service
from opencopilot.service.chat import chat_streaming_service
from opencopilot.service.chat.entities import ChatDeleteRequest
from opencopilot.service.chat.entities import ChatDeleteResponse
from opencopilot.service.chat.entities import ChatHistoryRequest
from opencopilot.service.chat.entities import ChatHistoryResponse
from opencopilot.service.chat.entities import ChatRequest
from opencopilot.service.chat.entities import ChatResponse
from opencopilot.service.chat.entities import ConversationsRequest
from opencopilot.service.chat.entities import ConversationsResponse
from opencopilot.callbacks import PromptBuilder

TAG = "Conversation"
router = APIRouter()
router.openapi_tags = [TAG]
router.title = "Conversation router"

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
    response_message_id: Optional[str] = Field(
        None,
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
    response_model=ConversationsResponse,
)
async def handle_get_conversations(
    user_id: str = Depends(validate_api_key_use_case.execute),
):
    users_repository = UsersRepositoryLocal()
    response = chat_conversations_service.execute(
        request=ConversationsRequest(user_id=user_id), users_repository=users_repository
    )
    return response


@router.post(
    "/conversations/{conversation_id}",
    summary="Send a message to the copilot and receive a non-streamed response.",
    tags=[TAG],
    response_model=ChatResponse,
)
async def handle_conversation(
    background_tasks: BackgroundTasks,
    api_request: Request,
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
        conversation_id=conversation_id,
        message=payload.message,
        response_message_id=payload.response_message_id,
        user_id=user_id,
    )

    history_repository = ConversationHistoryRepositoryLocal()
    logs_repository = ConversationLogsRepositoryLocal()
    users_repository = UsersRepositoryLocal()

    response: ChatResponse = await chat_service.execute(
        request,
        document_store.get_document_store(),
        history_repository,
        logs_repository,
        users_repository,
        api_request.app.copilot_callbacks,
    )

    background_tasks.add_task(
        track,
        TrackingEventType.CHAT_MESSAGE,
        api_request.headers.get("user-agent"),
        False,
    )
    return response


@router.post(
    "/conversations/{conversation_id}/stream",
    summary="Send a message to the copilot and stream the response.",
    response_description=STREAM_RESPONSE_DESCRIPTION,
    tags=[TAG],
)
async def handle_conversation_streaming(
    background_tasks: BackgroundTasks,
    api_request: Request,
    conversation_id: str = Path(..., description=CONVERSATION_ID_DESCRIPTION),
    payload: ConversationInput = Body(
        ..., description="Input and parameters for the conversation."
    ),
    user_id: str = Depends(validate_api_key_use_case.execute),
):
    request = ChatRequest(
        conversation_id=conversation_id,
        message=payload.message,
        response_message_id=payload.response_message_id,
        user_id=user_id,
    )

    history_repository = ConversationHistoryRepositoryLocal()
    logs_repository = ConversationLogsRepositoryLocal()
    users_repository = UsersRepositoryLocal()

    headers = {
        "X-Content-Type-Options": "nosniff",
        "Connection": "keep-alive",
    }

    background_tasks.add_task(
        track,
        TrackingEventType.CHAT_MESSAGE,
        api_request.headers.get("user-agent"),
        True,
    )

    return StreamingResponse(
        chat_streaming_service.execute(
            request,
            document_store.get_document_store(),
            history_repository,
            logs_repository,
            users_repository,
            api_request.app.copilot_callbacks,
        ),
        headers=headers,
        media_type="text/event-stream",
    )


@router.get(
    "/conversations/{conversation_id}",
    summary="Retrieve a conversation.",
    tags=[TAG],
    response_model=ChatHistoryResponse,
)
async def handle_get_conversation_history(
    conversation_id: str = Path(..., description="The ID of the conversation."),
    user_id: str = Depends(validate_api_key_use_case.execute),
):
    request = ChatHistoryRequest(
        conversation_id=conversation_id,
        user_id=user_id,
    )

    history_repository = ConversationHistoryRepositoryLocal()
    users_repository = UsersRepositoryLocal()

    response: ChatHistoryResponse = await chat_history_service.execute(
        request, history_repository, users_repository
    )
    return response


@router.delete(
    "/conversations/{conversation_id}",
    summary="Delete a conversation.",
    tags=[TAG],
    response_model=ChatDeleteResponse,
)
async def handle_delete_conversation_history(
    user_id: str = Depends(validate_api_key_use_case.execute),
    conversation_id: str = Path(..., description="The ID of the conversation."),
):
    users_repository = UsersRepositoryLocal()
    history_repository = ConversationHistoryRepositoryLocal()
    logs_repository = ConversationLogsRepositoryLocal()
    response = chat_delete_service.execute(
        request=ChatDeleteRequest(
            conversation_id=conversation_id,
            user_id=user_id,
        ),
        users_repository=users_repository,
        history_repository=history_repository,
        logs_repository=logs_repository,
    )
    return response
