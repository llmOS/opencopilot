from opencopilot.domain.chat.entities import ChatDeleteInput
from opencopilot.domain.chat.entities import ChatDeleteOutput
from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)
from opencopilot.repository.conversation_logs_repository import (
    ConversationLogsRepositoryLocal,
)
from opencopilot.repository.users_repository import UsersRepositoryLocal


def execute(
    data_input: ChatDeleteInput,
    users_repository: UsersRepositoryLocal,
    history_repository: ConversationHistoryRepositoryLocal,
    logs_repository: ConversationLogsRepositoryLocal,
) -> ChatDeleteOutput:
    conversations = users_repository.get_conversations(data_input.user_id)
    if str(data_input.conversation_id) in conversations:
        history_repository.remove_conversation(data_input.conversation_id)
        logs_repository.remove_conversation(data_input.conversation_id)
        users_repository.remove_conversation(
            conversation_id=data_input.conversation_id, user_id=data_input.user_id
        )
        return ChatDeleteOutput(response="OK")
    return ChatDeleteOutput(response="NOK")
