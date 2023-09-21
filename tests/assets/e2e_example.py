import os
from pathlib import Path
from uuid import UUID

from dotenv import load_dotenv
from langchain.schema import Document

from opencopilot import OpenCopilot

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

PROMPT_TEMPLATE = """
You are an Estonian Copilot.

As context to reply to the user you are given the following extracted parts of a long document, previous chat history, and a question from the user.

You only answer in Estonian language.

If you don"t know the answer, please ask the user to be more precise with their question in a polite manner. Don"t try to make up an answer if you do not know it or have no information about it in the context.
If the question is not related to the goals, politely inform the user that you are tuned to only answer questions related to the goals.
REMEMBER to always provide 3 example follow up questions that would be helpful for the user to continue the conversation.

=========
{context}
=========

{history}
User: {question}
Estonian copilot answer in Markdown:
"""

copilot = OpenCopilot(
    prompt=PROMPT_TEMPLATE,
    helicone_api_key=os.getenv("HELICONE_API_KEY"),
    auth_type=os.getenv("AUTH_TYPE"),
    jwt_client_id=os.getenv("JWT_CLIENT_ID"),
    jwt_client_secret=os.getenv("JWT_CLIENT_SECRET"),
)
copilot.add_local_files_dir("tests/assets/e2e_example_data")


@copilot.data_loader
def e2e_data_loader():
    return [
        Document(
            page_content="Estonian last president was Kersti Mock Kaljulaid",
            metadata={"source": "internet"}
        )
    ]


@copilot.prompt_builder
def prompt_builder(conversation_id: UUID, user_id: str, message: str) -> str:
    if "who is the prime minister" in message.lower():
        return PROMPT_TEMPLATE.format(
            context="Prime minister of Estonia is Kaja Mock Kallas",
            history="",
            question=message
        )
    return None


copilot()
