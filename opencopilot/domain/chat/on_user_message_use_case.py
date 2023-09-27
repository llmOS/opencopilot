from datetime import datetime
from typing import List

from langchain.schema import Document

from opencopilot.callbacks import ContextInput
from opencopilot.domain.chat import is_user_allowed_to_chat_use_case
from opencopilot.domain.chat.entities import ChatContext
from opencopilot.domain.chat.entities import MessageModel
from opencopilot.domain.chat.entities import UserMessageInput
from opencopilot.domain.chat.results import get_gpt_result_use_case
from opencopilot.domain.chat.utils import get_system_message
from opencopilot.logger import api_logger
from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)
from opencopilot.repository.conversation_logs_repository import (
    ConversationLogsRepositoryLocal,
)
from opencopilot.repository.documents.document_store import DocumentStore
from opencopilot.repository.users_repository import UsersRepositoryLocal
from opencopilot.service.error_responses import ForbiddenAPIError
from opencopilot.callbacks import CopilotCallbacks

logger = api_logger.get()


async def execute(
    domain_input: UserMessageInput,
    document_store: DocumentStore,
    history_repository: ConversationHistoryRepositoryLocal,
    logs_repository: ConversationLogsRepositoryLocal,
    users_repository: UsersRepositoryLocal,
    copilot_callbacks: CopilotCallbacks = None,
) -> MessageModel:
    if not is_user_allowed_to_chat_use_case.execute(
        domain_input.conversation_id,
        domain_input.user_id,
        history_repository,
        users_repository,
    ):
        raise ForbiddenAPIError()

    system_message = get_system_message()
    context = []
    if "{context}" in system_message:
        context = document_store.find(domain_input.message)
    custom_context: List[Document] = []
    if copilot_callbacks.context_builder:
        custom_context = await copilot_callbacks.context_builder(
            ContextInput(
                conversation_id=domain_input.conversation_id,
                user_id=domain_input.user_id,
                message=domain_input.message,
                history=history_repository.get_messages(domain_input.conversation_id),
            )
        )
    message_timestamp = datetime.now().timestamp()
    result = await get_gpt_result_use_case.execute(
        domain_input,
        system_message,
        ChatContext(local_context=context, custom_context=custom_context),
        logs_repository=logs_repository,
        history_repository=history_repository,
        copilot_callbacks=copilot_callbacks,
    )

    response_timestamp = datetime.now().timestamp()

    history_repository.save_history(
        domain_input.message,
        result,
        message_timestamp,
        response_timestamp,
        domain_input.conversation_id,
        domain_input.response_message_id,
    )
    users_repository.add_conversation(
        conversation_id=domain_input.conversation_id, user_id=domain_input.user_id
    )
    sources = [document.metadata.get("source") for document in context]

    return MessageModel(
        conversation_id=domain_input.conversation_id, content=result, sources=sources
    )
