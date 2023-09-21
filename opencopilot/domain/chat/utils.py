from dataclasses import dataclass
from typing import List
from uuid import UUID

from opencopilot import settings
from opencopilot.domain.chat.entities import UserMessageHistoryItem
from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)


@dataclass(frozen=True)
class History:
    template_with_history: str
    formatted_history: str


def add_history(
    template: str,
    conversation_id: UUID,
    history_repository: ConversationHistoryRepositoryLocal,
    message_history: List[UserMessageHistoryItem],
) -> History:
    history = _get_history(
        conversation_id=conversation_id,
        history_repository=history_repository,
        message_history=message_history,
    )
    history = history.replace("{", "{{").replace("}", "}}")
    return History(
        template_with_history=template.replace("{history}", history, 1),
        formatted_history=history,
    )


def _get_history(
    conversation_id: UUID,
    history_repository: ConversationHistoryRepositoryLocal,
    message_history: List[UserMessageHistoryItem],
) -> str:
    if message_history:
        return _format_message_history(message_history)
    return history_repository.get_history_for_prompt(
        conversation_id, settings.get().PROMPT_HISTORY_INCLUDED_COUNT
    )


def _format_message_history(history: List[UserMessageHistoryItem]) -> str:
    result = []
    for item in history:
        result.append(item.type.capitalize() + ": " + item.message)
    return "\n".join(result)


def get_system_message() -> str:
    return settings.get().PROMPT
