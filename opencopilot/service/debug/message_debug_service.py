from typing import Optional

from opencopilot.domain.debug import message_debug_use_case
from opencopilot.domain.debug.entities import TextWithTokens
from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)
from opencopilot.repository.conversation_logs_repository import (
    ConversationLogsRepositoryLocal,
)
from opencopilot.repository.users_repository import UsersRepositoryLocal
from opencopilot.service import utils
from opencopilot.service.debug.entities import GetMessageDebugResponse
from opencopilot.service.debug.entities import ValueWithTokens


def execute(
    conversation_id: str,
    message_id: str,
    history_repository: ConversationHistoryRepositoryLocal,
    logs_repository: ConversationLogsRepositoryLocal,
    users_repository: UsersRepositoryLocal,
    user_id: Optional[str] = None,
) -> GetMessageDebugResponse:
    domain_response = message_debug_use_case.execute(
        utils.get_uuid(conversation_id, "conversation_id"),
        message_id,
        history_repository,
        logs_repository,
        users_repository=users_repository,
        user_id=user_id,
    )
    return GetMessageDebugResponse(
        response="OK",
        prompt_template=_convert(domain_response.prompt_template),
        data_sources=domain_response.data_sources,
        user_question=_convert(domain_response.user_question),
        context=_convert(domain_response.context),
        chat_history=_convert(domain_response.chat_history),
        full_prompt=_convert(domain_response.full_prompt),
        llm_response=_convert(domain_response.llm_response),
    )


def _convert(value: Optional[TextWithTokens]) -> Optional[ValueWithTokens]:
    if not value:
        return None
    return ValueWithTokens(
        value=value.text,
        token_count=value.token_count,
    )
