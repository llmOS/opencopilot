from typing import Optional
from uuid import UUID

from opencopilot.logger import api_logger
from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)
from opencopilot.repository.users_repository import UsersRepositoryLocal
from opencopilot.service.chat.entities import ChatHistoryItem

logger = api_logger.get()


async def execute(
    conversation_id: UUID,
    user_id: Optional[str],
    history_repository: ConversationHistoryRepositoryLocal,
    users_repository: UsersRepositoryLocal,
) -> [ChatHistoryItem]:
    if not await is_user_conversation(conversation_id, user_id, users_repository):
        return []

    response = history_repository.get_history(conversation_id)
    return_value = []
    timer = 0
    for message in response:
        prompt_timestamp = (
            message["prompt_timestamp"] if "prompt_timestamp" in message else timer
        )
        response_timestamp = (
            message["response_timestamp"]
            if "response_timestamp" in message
            else timer + 1
        )
        timer = max(timer, prompt_timestamp, response_timestamp) + 2
        return_value = return_value + [
            ChatHistoryItem(
                content=message["prompt"],
                timestamp=prompt_timestamp,
                response_message_id=message["response_message_id"],
            ),
            ChatHistoryItem(
                content=message["response"],
                timestamp=response_timestamp,
                response_message_id=message["response_message_id"],
            ),
        ]

    return return_value


async def is_user_conversation(
    conversation_id: UUID,
    user_id: Optional[str],
    users_repository: UsersRepositoryLocal,
) -> bool:
    conversations = users_repository.get_conversations(user_id)
    if str(conversation_id) in conversations:
        return True
    return False
