from typing import Dict
from typing import List
from typing import Optional
from uuid import UUID

from opencopilot.domain.debug.entities import MessageDebugResult
from opencopilot.domain.debug.entities import TextWithTokens
from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)
from opencopilot.repository.conversation_logs_repository import (
    ConversationLogsRepositoryLocal,
)
from opencopilot.repository.users_repository import UsersRepositoryLocal
from opencopilot.service.error_responses import ForbiddenAPIError


def execute(
    conversation_id: UUID,
    message_id: str,
    history_repository: ConversationHistoryRepositoryLocal,
    logs_repository: ConversationLogsRepositoryLocal,
    users_repository: UsersRepositoryLocal,
    user_id: Optional[str] = None,
) -> MessageDebugResult:
    conversations = users_repository.get_conversations(user_id)
    if str(conversation_id) not in conversations:
        raise ForbiddenAPIError()

    history = history_repository.get_history(conversation_id)
    logs_history = logs_repository.get_logs_by_message(conversation_id, message_id)
    return MessageDebugResult(
        prompt_template=_get_logs_history_value(logs_history, "prompt_template"),
        data_sources=None,
        user_question=_get_history_value(history, message_id, "prompt"),
        context=_get_logs_history_value(logs_history, "context"),
        chat_history=_get_logs_history_value(logs_history, "history"),
        full_prompt=_get_logs_history_value(logs_history, "prompt_text"),
        llm_response=_get_history_value(history, message_id, "response"),
    )


def _get_history_value(
    history: List[Dict],
    message_id: str,
    value_key: str,
) -> Optional[TextWithTokens]:
    for h in history:
        if h.get("response_message_id") == message_id:
            return TextWithTokens(
                text=h.get(value_key),
                token_count=None,
            )

    return None


def _get_logs_history_value(
    history: List[Dict],
    value_key: str,
) -> Optional[TextWithTokens]:
    for h in history:
        if value := h.get(value_key):
            return TextWithTokens(
                text=value,
                token_count=h.get("token_count"),
            )
    return None
