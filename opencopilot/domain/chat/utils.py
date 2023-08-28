import os
from dataclasses import dataclass
from uuid import UUID
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback

from opencopilot.logger import api_logger
from opencopilot import settings
from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)

logger = api_logger.get()

RETRIEVAL_PROMPT_TEMPLATE = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""


@dataclass(frozen=True)
class History:
    template_with_history: str
    formatted_history: str


def add_history(
    template: str,
    chat_id: UUID,
    history_repository: ConversationHistoryRepositoryLocal,
) -> History:
    os.makedirs(settings.get().CONVERSATIONS_DIR, exist_ok=True)
    history = history_repository.get_prompt_history(
        chat_id, settings.get().PROMPT_HISTORY_INCLUDED_COUNT
    )
    history = history.replace("{", "{{").replace("}", "}}")
    return History(
        template_with_history=template.replace("{history}", history, 1),
        formatted_history=history,
    )


def get_system_message() -> str:
    with open(settings.get().PROMPT_FILE, "r") as f:
        return f.read()


def get_context_query(query: str, history: History) -> str:
    if settings.get().USE_CONVERSATIONAL_RETRIEVAL and history.formatted_history:
        try:
            llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k")
            prompt = RETRIEVAL_PROMPT_TEMPLATE.format(
                chat_history=history.formatted_history, question=query
            )
            logger.debug(f"PROMPT {prompt}")
            with get_openai_callback() as cb:
                llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k")
                query = llm.predict(prompt)
            logger.debug(cb)
        except:
            pass
    logger.debug(f"RETRIEVAL QUERY {query}")
    return query
