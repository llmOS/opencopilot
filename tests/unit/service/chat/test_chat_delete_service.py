import uuid
from unittest.mock import MagicMock

import pytest

from opencopilot.domain.chat.entities import ChatDeleteOutput
from opencopilot.service.chat import chat_delete_service as service
from opencopilot.service.chat.entities import ChatDeleteRequest
from opencopilot.service.chat.entities import ChatDeleteResponse
from opencopilot.service.error_responses import ForbiddenAPIError

REQUEST = ChatDeleteRequest(
    conversation_id=str(uuid.uuid4())
)


def test_success():
    service.chat_delete_use_case = MagicMock()
    service.chat_delete_use_case.execute.return_value = ChatDeleteOutput(response="OK")

    result = service.execute(
        request=REQUEST,
        users_repository=MagicMock(),
        history_repository=MagicMock(),
        logs_repository=MagicMock()
    )
    assert result == ChatDeleteResponse(response="OK")


def test_error():
    service.chat_delete_use_case = MagicMock()
    service.chat_delete_use_case.execute.return_value = ChatDeleteOutput(response="NOK")
    with pytest.raises(ForbiddenAPIError):
        service.execute(
            request=REQUEST,
            users_repository=MagicMock(),
            history_repository=MagicMock(),
            logs_repository=MagicMock()
        )
