from dataclasses import dataclass
from uuid import UUID

from opencopilot import settings
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
) -> History:
    history = history_repository.get_history_for_prompt(
        conversation_id, settings.get().PROMPT_HISTORY_INCLUDED_COUNT
    )
    history = history.replace("{", "{{").replace("}", "}}")
    return History(
        template_with_history=template.replace("{history}", history, 1),
        formatted_history=history,
    )


def get_system_message() -> str:
    return settings.get().PROMPT
