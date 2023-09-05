import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

from opencopilot import OpenCopilot

load_dotenv()

PROMPT = """Your are a Parrot Copilot.
Your purpose is to repeat what the user says, but in a different wording.
You can use the context and history to do so.

=========
{context}
=========

{history}
User: {question}
Parrot Copilot answer in Markdown:"""

llm = ChatOpenAI(
    temperature=0.0,
    openai_api_base="http://127.0.0.1:8000/v1",
    max_tokens=4096
)

copilot = OpenCopilot(
    prompt=PROMPT,
    copilot_name="oss_copilot",
    llm=llm,
    host=os.getenv("HOST"),
    auth_type=os.getenv("AUTH_TYPE"),
    weaviate_url=os.getenv("WEAVIATE_URL"),
    helicone_api_key=os.getenv("HELICONE_API_KEY"),
    jwt_client_id=os.getenv("JWT_CLIENT_ID") or "",
    jwt_client_secret=os.getenv("JWT_CLIENT_SECRET") or "",
    jwt_token_expiration_seconds=int(os.getenv("JWT_TOKEN_EXPIRATION_SECONDS") or "0")
)

copilot()
