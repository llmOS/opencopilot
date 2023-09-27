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
    """
    Builds a custom prompt based on the detected user intent.

    This function is decorated with @copilot.prompt_builder which means it will 
    be used to determine the prompt to pass to the OpenCopilot instance. The 
    function detects the intent of the incoming message and returns a specific 
    prompt based on the detected intent.

    Args:
    - conversation_id (UUID): Unique identifier for the conversation.
    - user_id (str): Unique identifier for the user.
    - message (str): The message received from the user.

    Returns:
    Optional[str]: A custom prompt based on the detected intent or None if 
                   the copilot should continue without any custom prompting
    """
    user_intent = intents.detect_intent(message)
    print(f"Intent {user_intent}")
    if user_intent == Intent.GREETING:
        return 'Say literally "HELLO".'
    return None


copilot()
