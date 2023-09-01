from opencopilot.domain.chat import get_chat_history_use_case
from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)
from opencopilot.repository.users_repository import UsersRepositoryLocal
from opencopilot.service.chat.entities import ChatHistoryRequest
from opencopilot.service.chat.entities import ChatHistoryResponse
from opencopilot.service.error_responses import ForbiddenAPIError
from opencopilot.service.utils import get_uuid


async def execute(
    request: ChatHistoryRequest,
    history_repository: ConversationHistoryRepositoryLocal,
    users_repository: UsersRepositoryLocal,
) -> ChatHistoryResponse:
    conversation_id = get_uuid(request.conversation_id, "conversation_id")
    messages = await get_chat_history_use_case.execute(
        conversation_id=conversation_id,
        user_id=request.user_id,
        history_repository=history_repository,
        users_repository=users_repository,
    )
    if not messages:
        raise ForbiddenAPIError()
    return ChatHistoryResponse(
        response="OK",
        conversation_id=str(conversation_id),
        messages=messages,
    )
