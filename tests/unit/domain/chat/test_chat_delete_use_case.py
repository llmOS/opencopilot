from unittest.mock import MagicMock
from uuid import UUID

from opencopilot.domain.chat import chat_delete_use_case as use_case
from opencopilot.domain.chat.entities import ChatDeleteInput
from opencopilot.domain.chat.entities import ChatDeleteOutput

CONVERSATION_ID = UUID("69f88a74-7a67-4336-b601-4cfbcaed55ef")
INVALID_CONVERSATION_ID = UUID("79f88a74-7a67-4336-b601-4cfbcaed55ef")
USER_ID = "user_id"


def test_remove_calls_repository():
    users_repository = MagicMock()
    users_repository.get_conversations.return_value = [str(CONVERSATION_ID)]
    history_repository = MagicMock()
    logs_repository = MagicMock()

    result = use_case.execute(
        data_input=ChatDeleteInput(
            conversation_id=CONVERSATION_ID,
            user_id=USER_ID
        ),
        users_repository=users_repository,
        history_repository=history_repository,
        logs_repository=logs_repository,
    )
    assert result == ChatDeleteOutput(response="OK")
    users_repository.remove_conversation.assert_called_with(
        conversation_id=CONVERSATION_ID,
        user_id=USER_ID
    )
    history_repository.remove_conversation.assert_called_with(
        CONVERSATION_ID
    )
    logs_repository.remove_conversation.assert_called_with(
        CONVERSATION_ID
    )


def test_remove_not_called_when_not_user_conversation():
    users_repository = MagicMock()
    users_repository.get_conversations.return_value = [str(CONVERSATION_ID)]
    history_repository = MagicMock()
    logs_repository = MagicMock()

    result = use_case.execute(
        data_input=ChatDeleteInput(
            conversation_id=INVALID_CONVERSATION_ID,
            user_id=USER_ID
        ),
        users_repository=users_repository,
        history_repository=history_repository,
        logs_repository=logs_repository
    )
    assert result == ChatDeleteOutput(response="NOK")
    users_repository.remove_conversation.assert_not_called()
    history_repository.remove_conversation.assert_not_called()
    logs_repository.remove_conversation.assert_not_called()
