from unittest.mock import MagicMock
from uuid import UUID

from opencopilot.domain.debug.entities import MessageDebugResult
from opencopilot.domain.debug.entities import TextWithTokens
from opencopilot.service.debug import message_debug_service as service
from opencopilot.service.debug.entities import GetMessageDebugResponse
from opencopilot.service.debug.entities import ValueWithTokens


def setup():
    service.api_logger = MagicMock()
    service.message_debug_use_case = MagicMock()
    service.utils = MagicMock()
    service.utils.get_uuid.return_value = UUID("2ba94f1d-c9e1-442a-954d-b681d989bd92")


def test_success():
    service.message_debug_use_case.execute.return_value = MessageDebugResult(
        prompt_template=TextWithTokens(
            text="prompt_template",
            token_count=12,
        ),
        data_sources=None,
        user_question=TextWithTokens(
            text="user_question",
            token_count=12,
        ),
        context=TextWithTokens(
            text="context",
            token_count=12,
        ),
        chat_history=TextWithTokens(
            text="chat_history",
            token_count=12,
        ),
        full_prompt=TextWithTokens(
            text="full_prompt",
            token_count=12,
        ),
        llm_response=TextWithTokens(
            text="llm_response",
            token_count=12,
        ),
    )
    response = service.execute(
        "conversation_id",
        "message_id",
        MagicMock(),
        MagicMock(),
        MagicMock(),
        "user_id"
    )
    assert response == GetMessageDebugResponse(
        response="OK",
        prompt_template=ValueWithTokens(
            value="prompt_template",
            token_count=12,
        ),
        data_sources=None,
        user_question=ValueWithTokens(
            value="user_question",
            token_count=12,
        ),
        context=ValueWithTokens(
            value="context",
            token_count=12,
        ),
        chat_history=ValueWithTokens(
            value="chat_history",
            token_count=12,
        ),
        full_prompt=ValueWithTokens(
            value="full_prompt",
            token_count=12,
        ),
        llm_response=ValueWithTokens(
            value="llm_response",
            token_count=12,
        ),
    )
