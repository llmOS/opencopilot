import json
import uuid
from typing import Optional
from typing import AsyncIterable

from opencopilot.domain.chat import on_user_message_streaming_use_case
from opencopilot.domain.chat.entities import UserMessageInput
from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)
from opencopilot.repository.conversation_logs_repository import (
    ConversationLogsRepositoryLocal,
)
from opencopilot.repository.documents.document_store import DocumentStore
from opencopilot.repository.users_repository import UsersRepositoryLocal
from opencopilot.service.chat.entities import ChatRequest
from opencopilot.service.utils import get_uuid
from opencopilot.callbacks import CopilotCallbacks


async def execute(
    request: ChatRequest,
    document_store: DocumentStore,
    history_repository: ConversationHistoryRepositoryLocal,
    logs_repository: ConversationLogsRepositoryLocal,
    users_repository: UsersRepositoryLocal,
    copilot_callbacks: CopilotCallbacks = None,
) -> AsyncIterable[str]:
    conversation_id = get_uuid(request.conversation_id, "conversation_id")
    async for chunk in on_user_message_streaming_use_case.execute(
        UserMessageInput(
            conversation_id=conversation_id,
            message=request.message,
            response_message_id=str(uuid.uuid4()),
            user_id=request.user_id,
        ),
        document_store,
        history_repository,
        logs_repository,
        users_repository,
        copilot_callbacks,
    ):
        data = chunk.to_dict()
        yield f"{json.dumps(data)}\n"
