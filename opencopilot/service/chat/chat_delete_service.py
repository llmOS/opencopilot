from opencopilot.domain.chat import chat_delete_use_case
from opencopilot.domain.chat.entities import ChatDeleteInput
from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)
from opencopilot.repository.conversation_logs_repository import (
    ConversationLogsRepositoryLocal,
)
from opencopilot.repository.users_repository import UsersRepositoryLocal
from opencopilot.service.chat.entities import ChatDeleteRequest
from opencopilot.service.chat.entities import ChatDeleteResponse
from opencopilot.service.error_responses import ForbiddenAPIError
from opencopilot.service.utils import get_uuid


def execute(
    request: ChatDeleteRequest,
    users_repository: UsersRepositoryLocal,
    history_repository: ConversationHistoryRepositoryLocal,
    logs_repository: ConversationLogsRepositoryLocal,
) -> ChatDeleteResponse:
    conversation_id = get_uuid(request.conversation_id, "conversation_id")
    result = chat_delete_use_case.execute(
        data_input=ChatDeleteInput(
            conversation_id=conversation_id, user_id=request.user_id
        ),
        users_repository=users_repository,
        history_repository=history_repository,
        logs_repository=logs_repository,
    )
    if result.response == "NOK":
        raise ForbiddenAPIError()
    return ChatDeleteResponse(response=result.response)
