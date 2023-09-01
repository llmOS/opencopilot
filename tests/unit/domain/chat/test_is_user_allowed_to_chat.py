from unittest.mock import MagicMock
from uuid import UUID

from opencopilot.domain.chat import is_user_allowed_to_chat_use_case as use_case

CONVERSATION_ID = UUID("498a71c1-babe-4e38-b686-8917d66f0e8d")
INVALID_CONVERSATION_ID = UUID("598a71c1-babe-4e38-b686-8917d66f0e8d")


def test_conversation_does_not_exist():
    history_repository = MagicMock()
    history_repository.get_history.return_value = []
    result = use_case.execute(
        conversation_id=CONVERSATION_ID,
        user_id="user_id",
        history_repository=history_repository,
        users_repository=MagicMock()
    )
    assert result


def test_conversation_exists_belongs_to_user():
    history_repository = MagicMock()
    history_repository.get_history.return_value = [{"mock": "mock"}]

    users_repository = MagicMock()
    users_repository.get_conversations.return_value = [str(CONVERSATION_ID)]
    result = use_case.execute(
        conversation_id=CONVERSATION_ID,
        user_id="user_id",
        history_repository=history_repository,
        users_repository=users_repository
    )
    assert result


def test_conversation_exists_not_belongs_to_user():
    history_repository = MagicMock()
    history_repository.get_history.return_value = [{"mock": "mock"}]

    users_repository = MagicMock()
    users_repository.get_conversations.return_value = [str(INVALID_CONVERSATION_ID)]
    result = use_case.execute(
        conversation_id=CONVERSATION_ID,
        user_id="user_id",
        history_repository=history_repository,
        users_repository=users_repository
    )
    assert not result
