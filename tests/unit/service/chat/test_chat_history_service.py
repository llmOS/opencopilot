import asyncio
import uuid
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

import pytest

from opencopilot.service.chat import chat_history_service as service
from opencopilot.service.chat.entities import ChatHistoryItem
from opencopilot.service.chat.entities import ChatHistoryRequest
from opencopilot.service.chat.entities import ChatHistoryResponse
from opencopilot.service.error_responses import ForbiddenAPIError

MESSAGES = [ChatHistoryItem(content="mock", timestamp=1, response_message_id="rmi")]


def setup_function():
    service.get_chat_history_use_case = MagicMock()
    service.get_chat_history_use_case.execute = AsyncMock(return_value=MESSAGES)


@pytest.mark.asyncio
async def test_returns_ok():
    conversation_id = uuid.uuid4()
    result = await service.execute(
        request=ChatHistoryRequest(
            conversation_id=str(conversation_id),
        ),
        history_repository=MagicMock(),
        users_repository=MagicMock(),
    )
    assert result == ChatHistoryResponse(
        response="OK",
        conversation_id=str(conversation_id),
        messages=MESSAGES,
    )


@pytest.mark.asyncio
async def test_raises_forbidden():
    service.get_chat_history_use_case.execute = AsyncMock(return_value=[])

    conversation_id = uuid.uuid4()
    with pytest.raises(ForbiddenAPIError):
        await service.execute(
            request=ChatHistoryRequest(
                conversation_id=str(conversation_id),
            ),
            history_repository=MagicMock(),
            users_repository=MagicMock(),
        )
