from uuid import UUID
from typing import Callable
from typing import Optional
from opencopilot.repository.documents.document_store import DocumentStore

PromptBuilder = Callable[[str, UUID, str], Optional[str]]


class CopilotCallbacks:
    prompt_builder: Optional[PromptBuilder] = None
