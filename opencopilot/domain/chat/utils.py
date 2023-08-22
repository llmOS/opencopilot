import os
from dataclasses import dataclass
from uuid import UUID

from opencopilot import settings
from opencopilot.repository.conversation_history_repository import ConversationHistoryRepositoryLocal


@dataclass(frozen=True)
class History:
    template_with_history: str
    formatted_history: str


def add_history(
        template: str,
        chat_id: UUID,
        history_repository: ConversationHistoryRepositoryLocal,
) -> History:
    os.makedirs(settings.get().CONVERSATIONS_DIR, exist_ok=True)
    history = history_repository.get_prompt_history(
        chat_id, settings.get().PROMPT_HISTORY_INCLUDED_COUNT)
    history = history.replace("{", "{{").replace("}", "}}")
    return History(
        template_with_history=template.replace("{history}", history, 1),
        formatted_history=history,
    )


def get_system_message() -> str:
    with open(settings.get().PROMPT_FILE, "r") as f:
        return f.read()
