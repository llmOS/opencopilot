from typing import List
from typing import Callable
from typing import Optional
from langchain.schema import BaseMessage
from opencopilot.repository.documents.document_store import DocumentStore

PromptBuilder = Callable[[str, List[BaseMessage], DocumentStore], Optional[str]]


class Callbacks:
    prompt_builder: Optional[PromptBuilder] = None
