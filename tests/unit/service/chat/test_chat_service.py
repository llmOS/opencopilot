import pytest
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from uuid import UUID

from opencopilot.domain.chat.entities import MessageModel
from opencopilot.service.chat import chat_service as service
from opencopilot.service.chat.entities import ChatRequest
from opencopilot.service.chat.entities import ChatResponse

CONVERSATION_ID = UUID("5a78244b-5c12-4366-b16a-00799bce7040")
MESSAGE_ID = UUID("6a09629f-0ecd-4db6-96ca-ffa6be6d3061")


def setup():
    service.on_user_message_use_case = MagicMock()
    service.on_user_message_use_case.execute = AsyncMock(
        return_value=MessageModel(
            conversation_id=CONVERSATION_ID,
            content="mock content",
            sources=[]
        )
    )
    service.get_uuid = MagicMock()
    service.get_uuid.return_value = CONVERSATION_ID

    service.uuid = MagicMock()
    service.uuid.uuid4.return_value = MESSAGE_ID


@pytest.mark.asyncio
async def test_success():
    response = await service.execute(
        ChatRequest(
            conversation_id=str(CONVERSATION_ID),
            message="what's up",
        ),
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock()
    )
    assert response == ChatResponse(
        response="OK",
        response_message_id=str(MESSAGE_ID),
        copilot_message="mock content",
        sources=[],
    )
