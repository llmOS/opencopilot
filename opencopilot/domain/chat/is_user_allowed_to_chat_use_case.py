from typing import Optional
from uuid import UUID

from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)
from opencopilot.repository.users_repository import UsersRepositoryLocal


def execute(
    conversation_id: UUID,
    user_id: Optional[str],
    history_repository: ConversationHistoryRepositoryLocal,
    users_repository: UsersRepositoryLocal,
) -> bool:
    conversation = history_repository.get_history(conversation_id)
    if not conversation:
        return True
    elif _is_user_conversation(conversation_id, user_id, users_repository):
        return True
    return False


def _is_user_conversation(
    conversation_id: UUID,
    user_id: Optional[str],
    users_repository: UsersRepositoryLocal,
) -> bool:
    conversations = users_repository.get_conversations(user_id)
    if str(conversation_id) in conversations:
        return True
    return False
