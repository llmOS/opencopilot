import asyncio
import json
from datetime import datetime
from typing import AsyncGenerator
from typing import List

from langchain.schema import Document

from opencopilot import settings
from opencopilot.domain.chat import is_user_allowed_to_chat_use_case
from opencopilot.domain.chat.entities import LoadingMessage
from opencopilot.domain.chat.entities import StreamingChunk
from opencopilot.domain.chat.entities import UserMessageInput
from opencopilot.domain.chat.results import get_gpt_result_use_case
from opencopilot.domain.chat.utils import get_system_message
from opencopilot.domain.errors import CopilotRuntimeError
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
from opencopilot.utils.callbacks.callback_handler import (
    CustomAsyncIteratorCallbackHandler,
)
from opencopilot.callbacks import CopilotCallbacks

logger = api_logger.get()


async def execute(
    domain_input: UserMessageInput,
    document_store: DocumentStore,
    history_repository: ConversationHistoryRepositoryLocal,
    logs_repository: ConversationLogsRepositoryLocal,
    users_repository: UsersRepositoryLocal,
    copilot_callbacks: CopilotCallbacks = None,
) -> AsyncGenerator[StreamingChunk, None]:
    if not is_user_allowed_to_chat_use_case.execute(
        domain_input.conversation_id,
        domain_input.user_id,
        history_repository,
        users_repository,
    ):
        raise ForbiddenAPIError()

    system_message = get_system_message()

    context = _get_context(domain_input, system_message, document_store)
    message_timestamp = datetime.now().timestamp()

    streaming_callback = CustomAsyncIteratorCallbackHandler()

    task = asyncio.create_task(
        get_gpt_result_use_case.execute(
            domain_input,
            system_message,
            context,
            logs_repository=logs_repository,
            history_repository=history_repository,
            copilot_callbacks=copilot_callbacks,
            streaming_callback=streaming_callback,
        )
    )

    result = ""
    is_metadata_sent: bool = False
    try:
        async for callback_result in streaming_callback.aiter():
            parsed = json.loads(callback_result)
            if token := parsed.get("token"):
                response = StreamingChunk(
                    conversation_id=domain_input.conversation_id,
                    text=token,
                    sources=[],
                )
                if not is_metadata_sent:
                    yield _include_metadata(response, domain_input.response_message_id)
                    is_metadata_sent = True
                else:
                    yield response
            if loading_message := parsed.get("loading_message"):
                yield StreamingChunk(
                    conversation_id=domain_input.conversation_id,
                    text="",
                    sources=[],
                    loading_message=LoadingMessage.from_dict(loading_message),
                )
        await task
        result = task.result()
    except CopilotRuntimeError as exc:
        logger.error(f"{type(exc).__name__}: {exc.message}")
        yield StreamingChunk(
            conversation_id=domain_input.conversation_id,
            text="",
            sources=[],
            error=f"{type(exc).__name__}: {exc.message}",
        )
    except Exception as exc:
        logger.error(f"Stream error: {exc}")
        yield StreamingChunk(
            conversation_id=domain_input.conversation_id,
            text="",
            sources=[],
            error=f"OpenAI error: {type(exc).__name__}",
        )
    finally:
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


def _get_context(
    domain_input: UserMessageInput, system_message: str, document_store: DocumentStore
) -> List[Document]:
    # TODO: handle context length and all the edge cases somehow a bit better
    context = []
    if "{context}" in system_message:
        context = []
        context.extend(
            document_store.find(
                domain_input.message,
                k=settings.get().MAX_CONTEXT_DOCUMENTS_COUNT - len(context),
            )
        )
    return context


def _include_metadata(
    chunk: StreamingChunk, response_message_id: str
) -> StreamingChunk:
    new_chunk = StreamingChunk(
        conversation_id=chunk.conversation_id,
        text=chunk.text,
        sources=chunk.sources,
        error=chunk.error,
        loading_message=chunk.loading_message,
        response_message_id=response_message_id,
    )
    return new_chunk
