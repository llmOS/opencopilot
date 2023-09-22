from typing import List
from typing import Tuple

from langchain import PromptTemplate
from langchain.chat_models.base import BaseChatModel
from langchain.schema import Document
from langchain.schema import HumanMessage
from openai import OpenAIError

from opencopilot import settings
from opencopilot.callbacks import CopilotCallbacks
from opencopilot.domain.chat import get_token_count_use_case
from opencopilot.domain.chat import utils
from opencopilot.domain.chat.entities import ChatContext
from opencopilot.domain.chat.entities import UserMessageInput
from opencopilot.domain.chat.results import format_context_documents_use_case
from opencopilot.domain.chat.results import get_llm
from opencopilot.domain.errors import OpenAIRuntimeError
from opencopilot.logger import api_logger
from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)
from opencopilot.repository.conversation_logs_repository import (
    ConversationLogsRepositoryLocal,
)
from opencopilot.utils.callbacks.callback_handler import (
    CustomAsyncIteratorCallbackHandler,
)

logger = api_logger.get()


async def execute(
    domain_input: UserMessageInput,
    system_message: str,
    context: ChatContext,
    logs_repository: ConversationLogsRepositoryLocal,
    history_repository: ConversationHistoryRepositoryLocal,
    copilot_callbacks: CopilotCallbacks = None,
    streaming_callback: CustomAsyncIteratorCallbackHandler = None,
) -> str:
    llm = get_llm.execute(
        domain_input.user_id, streaming=streaming_callback is not None
    )

    history = utils.add_history(
        template=system_message,
        conversation_id=domain_input.conversation_id,
        history_repository=history_repository,
        message_history=domain_input.message_history,
    )
    logs_repository.log_history(
        domain_input.conversation_id,
        domain_input.message,
        history.formatted_history,
        domain_input.response_message_id,
        token_count=get_token_count_use_case.execute(history.formatted_history, llm),
    )

    prompt_text = None
    if copilot_callbacks and copilot_callbacks.prompt_builder:
        prompt_text = copilot_callbacks.prompt_builder(
            conversation_id=domain_input.conversation_id,
            user_id=domain_input.user_id,
            message=domain_input.message,
        )

    if not prompt_text:
        prompt_text = _get_prompt_text(
            domain_input,
            history.template_with_history,
            context,
            llm,
            logs_repository,
        )

    logs_repository.log_prompt_text(
        domain_input.conversation_id,
        domain_input.message,
        prompt_text,
        domain_input.response_message_id,
        token_count=get_token_count_use_case.execute(prompt_text, llm),
    )
    logs_repository.log_prompt_template(
        domain_input.conversation_id,
        domain_input.message,
        system_message,
        domain_input.response_message_id,
        token_count=get_token_count_use_case.execute(
            system_message, llm, is_use_cache=True
        ),
    )

    messages = [HumanMessage(content=prompt_text)]
    try:
        result_message = await llm.agenerate(
            [messages],
            callbacks=[streaming_callback] if streaming_callback is not None else None,
            stream=streaming_callback is not None,
        )
        result = result_message.generations[0][0].text
        return result
    except OpenAIError as exc:
        raise OpenAIRuntimeError(exc.user_message)


def _get_prompt_text(
    domain_input: UserMessageInput,
    template_with_history: str,
    chat_context: ChatContext,
    llm: BaseChatModel,
    logs_repository: ConversationLogsRepositoryLocal,
) -> str:
    # Almost duplicated with get_local_llm_result_use_case._get_prompt_text
    context, context_documents_count = _get_context(chat_context.local_context, llm)
    prompt_text = ""
    if "{custom_context}" in template_with_history:
        if chat_context.custom_context:
            formatted_prompt = template_with_history
            custom_context, custom_context_documents_count = _get_context(
                chat_context.custom_context, llm
            )
            formatted_prompt = formatted_prompt.replace(
                "{custom_context}", custom_context
            )
            if (
                get_token_count_use_case.execute(formatted_prompt, llm)
                < settings.get().get_max_token_count()
            ):
                template_with_history = formatted_prompt
            else:
                logger.warning("Ignoring custom context")
                template_with_history = template_with_history.replace(
                    "{custom_context}", ""
                )
        else:
            template_with_history = template_with_history.replace(
                "{custom_context}", ""
            )
    if "{context}" in template_with_history:
        prompt = PromptTemplate(
            template=template_with_history, input_variables=["context", "question"]
        )

        prompt_text = prompt.format_prompt(
            **{"context": context, "question": domain_input.message}
        ).to_string()

        if (
            get_token_count_use_case.execute(prompt_text, llm)
            > settings.get().get_max_token_count()
        ):
            prompt_text = ""
        logs_repository.log_context(
            domain_input.conversation_id,
            domain_input.message,
            chat_context.local_context[0:context_documents_count],
            domain_input.response_message_id,
            token_count=get_token_count_use_case.execute(context, llm),
        )
    if not prompt_text:
        prompt = PromptTemplate(
            template=template_with_history, input_variables=["context", "question"]
        )
        prompt_text = prompt.format_prompt(
            **{"context": "", "question": domain_input.message}
        ).to_string()
    return prompt_text


def _get_context(
    documents: List[Document],
    llm: BaseChatModel,
    #  TODO: make threshold adjustable
) -> Tuple[str, int]:
    while len(documents):
        context = format_context_documents_use_case.execute(documents)
        token_count = get_token_count_use_case.execute(context, llm)
        # Naive solution: leaving 25% for non-context in prompt
        if token_count < (settings.get().get_max_token_count() * 0.75):
            return context, len(documents)
        documents = documents[:-1]
    return "", 0
