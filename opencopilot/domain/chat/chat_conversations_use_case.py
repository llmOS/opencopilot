from opencopilot.domain.chat.entities import ChatConversationsInput
from opencopilot.domain.chat.entities import ChatConversationsOutput
from opencopilot.repository.users_repository import UsersRepositoryLocal


def execute(
    data_input: ChatConversationsInput, users_repository: UsersRepositoryLocal
) -> ChatConversationsOutput:
    result = users_repository.get_conversations(data_input.user_id)
    return ChatConversationsOutput(conversations=result)
