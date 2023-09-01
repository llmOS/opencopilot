import uuid
from unittest.mock import MagicMock

import pytest

from opencopilot.domain.chat import on_user_message_streaming_use_case as use_case
from opencopilot.domain.chat.entities import UserMessageInput
from opencopilot.service.error_responses import ForbiddenAPIError


@pytest.mark.asyncio
async def test_not_allowed_to_chat():
    use_case.is_user_allowed_to_chat_use_case = MagicMock()
    use_case.is_user_allowed_to_chat_use_case.execute.return_value = False

    with pytest.raises(ForbiddenAPIError):
        async for _ in use_case.execute(
            domain_input=UserMessageInput(
                chat_id=uuid.uuid4(),
                message="msg",
                response_message_id="rmi"
            ),
            document_store=MagicMock(),
            history_repository=MagicMock(),
            logs_repository=MagicMock(),
            users_repository=MagicMock()
        ):
            pass
