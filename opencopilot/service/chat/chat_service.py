import uuid

from opencopilot.domain.chat import on_user_message_use_case
from opencopilot.domain.chat.entities import UserMessageInput
from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)
from opencopilot.repository.conversation_logs_repository import (
    ConversationLogsRepositoryLocal,
)
from opencopilot.repository.documents.document_store import DocumentStore
from opencopilot.repository.users_repository import UsersRepositoryLocal
from opencopilot.service.chat.entities import ChatRequest
from opencopilot.service.chat.entities import ChatResponse
from opencopilot.service.utils import get_uuid


async def execute(
    request: ChatRequest,
    document_store: DocumentStore,
    history_repository: ConversationHistoryRepositoryLocal,
    logs_repository: ConversationLogsRepositoryLocal,
    users_repository: UsersRepositoryLocal
) -> ChatResponse:
    chat_id = get_uuid(request.chat_id, "chat_id")
    domain_response = await on_user_message_use_case.execute(
        UserMessageInput(
            chat_id=chat_id,
            message=request.message,
            response_message_id=request.response_message_id or str(uuid.uuid4()),
            email=request.email,
        ),
        document_store,
        history_repository,
        logs_repository=logs_repository,
        users_repository=users_repository
    )
    return ChatResponse(
        response="OK",
        chat_id=str(chat_id),
        message=domain_response.content,
        sources=domain_response.sources,
    )
