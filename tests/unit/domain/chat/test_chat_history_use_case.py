from unittest.mock import MagicMock
from uuid import UUID

import pytest

from opencopilot.domain.chat import get_chat_history_use_case as use_case
from opencopilot.repository.conversation_history_repository import \
    ConversationHistoryRepositoryLocal
from opencopilot.repository.users_repository import UsersRepositoryLocal
from opencopilot.service.chat.entities import ChatHistoryItem

USER_ID = "user_id"
VALID_CONVERSATION_ID = UUID("1e1bbdbb-795a-40d7-807e-afd69a096d27")
INVALID_CONVERSATION_ID = UUID("2e1bbdbb-795a-40d7-807e-afd69a096d27")

history_repository: ConversationHistoryRepositoryLocal
users_repository: UsersRepositoryLocal


def setup_function():
    global history_repository
    history_repository = MagicMock()
    history_repository.get_history.return_value = [
        {
            "prompt_timestamp": 1693482043,
            "response_timestamp": 1693482044,
            "prompt": "p1",
            "response": "r1",
        }
    ]

    global users_repository
    users_repository = MagicMock()
    users_repository.get_conversations.return_value = [str(VALID_CONVERSATION_ID)]


@pytest.mark.asyncio
async def test_chat_belongs_to_user():
    result = await use_case.execute(
        chat_id=VALID_CONVERSATION_ID,
        user_id=USER_ID,
        history_repository=history_repository,
        users_repository=users_repository
    )
    assert result == [
        ChatHistoryItem(content='p1', timestamp=1693482043),
        ChatHistoryItem(content='r1', timestamp=1693482044)
    ]


@pytest.mark.asyncio
async def test_chat_no_belongs_to_user():
    users_repository.get_conversations.return_value = [str(INVALID_CONVERSATION_ID)]
    result = await use_case.execute(
        chat_id=VALID_CONVERSATION_ID,
        user_id=USER_ID,
        history_repository=history_repository,
        users_repository=users_repository
    )
    assert result == []
