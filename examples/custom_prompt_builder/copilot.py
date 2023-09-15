from uuid import UUID
from opencopilot import OpenCopilot

from typing import Optional

import intents
from intents import Intent

PROMPT = """
You are a helpful copilot.

{context}

{history}

{question}
"""

copilot = OpenCopilot(prompt=PROMPT)


@copilot.prompt_builder
def build_prompt(conversation_id: UUID, user_id: str, message: str) -> Optional[str]:
    user_intent = intents.detect_intent(message)
    if user_intent == Intent.GREETING:
        return 'Say literally "HELLO".'
    return None


copilot()
