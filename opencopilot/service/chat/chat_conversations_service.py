from opencopilot.domain.chat import chat_conversations_use_case
from opencopilot.domain.chat.entities import ChatConversationsInput
from opencopilot.repository.users_repository import UsersRepositoryLocal
from opencopilot.service.chat.entities import ConversationsRequest
from opencopilot.service.chat.entities import ConversationsResponse


def execute(
    request: ConversationsRequest,
    users_repository: UsersRepositoryLocal,
) -> ConversationsResponse:
    result = chat_conversations_use_case.execute(
        data_input=ChatConversationsInput(
            user_id=request.user_id,
        ),
        users_repository=users_repository,
    )
    return ConversationsResponse(response="OK", conversation_ids=result.conversations)
