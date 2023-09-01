from unittest.mock import MagicMock
from uuid import UUID

import pytest

from opencopilot.domain.debug import message_debug_use_case as use_case
from opencopilot.domain.debug.entities import MessageDebugResult
from opencopilot.domain.debug.entities import TextWithTokens
from opencopilot.service.error_responses import ForbiddenAPIError


def test_not_authorized():
    users_repository = MagicMock()
    users_repository.get_conversations.return_value = [
        "0fc265bb-7075-4060-bb0d-d246984836c3"
    ]
    with pytest.raises(ForbiddenAPIError):
        use_case.execute(
            UUID("0fc265bb-7075-4060-bb0d-d246984836c2"),
            "dc739efa-64ec-4bb1-be4b-0548471ce0ea",
            MagicMock(),
            MagicMock(),
            users_repository=users_repository,
        )


def test_success():
    message_id = "dc739efa-64ec-4bb1-be4b-0548471ce0ea"
    history_repository = MagicMock()
    history_repository.get_history.return_value = [
        {
            "prompt": "question-1",
            "response": "response-1",
            "prompt_timestamp": 1689839112.966415,
            "response_timestamp": 1689839128.582073,
            "response_message_id": "96dedd98-d770-4fba-a15e-b393e1489721"
        },
        {
            "prompt": "question-2",
            "response": "response-2",
            "prompt_timestamp": 1689839420.298775,
            "response_timestamp": 1689839431.46836,
            "response_message_id": message_id
        }
    ]
    logs_repository = MagicMock()
    logs_repository.get_logs_by_message.return_value = [
        {"response_message_id": message_id, "message": "question-2",
         "context": "[{\"page_content\": \"mock-content\", \"metadata\": {\"source\": \"mock-source\", \"title\": \"mock-title\"}}]",
         "token_count": 1070},
        {"response_message_id": message_id, "message": "question-2",
         "prompt_text": "mock-full-prompt",
         "token_count": 1909},
        {"response_message_id": message_id, "message": "question-2",
         "history": "mock-history",
         "token_count": 212},
    ]
    users_repository = MagicMock()
    users_repository.get_conversations.return_value = [
        "0fc265bb-7075-4060-bb0d-d246984836c2"
    ]
    response = use_case.execute(
        UUID("0fc265bb-7075-4060-bb0d-d246984836c2"),
        message_id,
        history_repository,
        logs_repository,
        users_repository=users_repository,
    )
    assert response == MessageDebugResult(
        prompt_template=None,
        data_sources=None,
        user_question=TextWithTokens(
            text="question-2",
            token_count=None,
        ),
        context=TextWithTokens(
            text="[{\"page_content\": \"mock-content\", \"metadata\": {\"source\": \"mock-source\", \"title\": \"mock-title\"}}]",
            token_count=1070,
        ),
        chat_history=TextWithTokens(
            text="mock-history",
            token_count=212,
        ),
        full_prompt=TextWithTokens(
            text="mock-full-prompt",
            token_count=1909,
        ),
        llm_response=TextWithTokens(
            text="response-2",
            token_count=None,
        ),
    )
