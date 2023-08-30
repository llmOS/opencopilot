import pytest
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from uuid import UUID

from opencopilot.domain.chat.entities import MessageModel
from opencopilot.service.chat import chat_service as service
from opencopilot.service.chat.entities import ChatRequest
from opencopilot.service.chat.entities import ChatResponse

CHAT_ID = UUID("5a78244b-5c12-4366-b16a-00799bce7040")


def setup():
    service.on_user_message_use_case = MagicMock()
    service.on_user_message_use_case.execute = AsyncMock(
        return_value=MessageModel(
            chat_id=CHAT_ID,
            content="mock content",
            sources=[]
        )
    )
    service.get_uuid = MagicMock()
    service.get_uuid.return_value = CHAT_ID


@pytest.mark.asyncio
async def test_success():
    response = await service.execute(
        ChatRequest(
            chat_id=str(CHAT_ID),
            message="what's up",
        ),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock()
    )
    assert response == ChatResponse(
        response="OK",
        chat_id=str(CHAT_ID),
        message="mock content",
    )
