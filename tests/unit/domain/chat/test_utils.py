from unittest.mock import MagicMock
from uuid import UUID

from opencopilot.domain.chat import utils
from opencopilot.domain.chat.entities import UserMessageHistoryItem
from opencopilot.domain.chat.utils import History
from opencopilot.repository.conversation_history_repository import \
    ConversationHistoryRepositoryLocal
from opencopilot.settings import Settings

TEMPLATE = """Mock
{history}
"""

CONVERSATION_ID = UUID("5ef320cf-eb77-4b75-80e3-a21d0fe674d9")

history_repository: ConversationHistoryRepositoryLocal


def setup_function():
    global history_repository
    history_repository = MagicMock()
    history_repository.get_history_for_prompt.return_value = ""

    utils.settings = MagicMock()
    utils.settings.get.return_value = Settings(
        COPILOT_NAME="str",
        HOST="str",
        API_PORT=123,
        ENVIRONMENT="str",
        ALLOWED_ORIGINS="str",
        LLM="str",
        EMBEDDING_MODEL="str",
    )


def test_add_history_no_message_history_no_history():
    result = utils.add_history(
        template=TEMPLATE,
        conversation_id=CONVERSATION_ID,
        history_repository=history_repository,
        message_history=[]
    )
    assert result == History(
        template_with_history="Mock\n\n",
        formatted_history=""
    )


def test_add_history_no_message_history_has_history():
    history_repository.get_history_for_prompt.return_value = "Mock History"
    result = utils.add_history(
        template=TEMPLATE,
        conversation_id=CONVERSATION_ID,
        history_repository=history_repository,
        message_history=[]
    )
    assert result == History(
        template_with_history="Mock\nMock History\n",
        formatted_history="Mock History"
    )


def test_add_history_has_message_history_no_history():
    result = utils.add_history(
        template=TEMPLATE,
        conversation_id=CONVERSATION_ID,
        history_repository=history_repository,
        message_history=[
            UserMessageHistoryItem(type="human", message="hello"),
            UserMessageHistoryItem(type="ai", message="world"),
        ]
    )
    assert result == History(
        template_with_history="Mock\nHuman: hello\nAi: world\n",
        formatted_history="Human: hello\nAi: world"
    )
