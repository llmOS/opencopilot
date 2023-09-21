from dataclasses import dataclass
from typing import Awaitable
from typing import List
from typing import Union
from uuid import UUID
from typing import Callable
from typing import Optional

from langchain.schema import AIMessage
from langchain.schema import Document
from langchain.schema import HumanMessage


@dataclass(frozen=True)
class ContextInput:
    conversation_id: UUID
    user_id: str
    message: str
    history: List[Union[HumanMessage, AIMessage]]


PromptBuilder = Callable[[UUID, str, str], Optional[str]]
ContextBuilder = Callable[[ContextInput], Awaitable[List[Document]]]


class CopilotCallbacks:
    prompt_builder: Optional[PromptBuilder] = None
    context_builder: Optional[ContextBuilder] = None
