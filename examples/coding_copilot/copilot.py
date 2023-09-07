"""
Coding copilot

Prerequisite:
Before using this module, users need to run CodeLlama LLM:

    opencopilot run codellama-[7, 13, 34]b

Key Components:
- OpenCopilot: Main class for interacting with the Opencopilot service.
- LocalLLM: A local instance of the language model used for code generation.
- HuggingFaceEmbeddings: Used for generating embeddings based on a model from the HuggingFace model hub.
- PROMPT: The template used by OpenCopilot for generating code based on given coding questions.

Environment Variables:
- HOST: The host URL for the OpenCopilot service.
- AUTH_TYPE: The authentication method used for the service.
- HELICONE_API_KEY: API key for the Helicone service.
- JWT_CLIENT_ID and JWT_CLIENT_SECRET: Credentials for JWT authentication.
- JWT_TOKEN_EXPIRATION_SECONDS: Expiration time for JWT tokens.

Usage:
Simply run and use `opencopilot chat` CLI to query the code copilot.
"""

import os
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings

from opencopilot import OpenCopilot
from opencopilot.domain.chat.models import LocalLLM

load_dotenv()

PROMPT = """{history}
[INST] Write code to solve the following coding problem that obeys the constraints and passes the example test cases. Relevant information: {context}. Please wrap your code answer using ```:
{question}
[/INST]
"""

llm = LocalLLM(
    temperature=0.0,
    llm_url="http://127.0.0.1:8000/",
)

embeddings = HuggingFaceEmbeddings(model_name="thenlper/gte-base")

copilot = OpenCopilot(
    prompt=PROMPT,
    question_template="[INST]{question}[/INST]",
    response_template="{response}",
    copilot_name="codellama_copilot",
    llm=llm,    
    embedding_model=embeddings,
    host=os.getenv("HOST"),
    auth_type=os.getenv("AUTH_TYPE"),
    helicone_api_key=os.getenv("HELICONE_API_KEY"),
    jwt_client_id=os.getenv("JWT_CLIENT_ID") or "",
    jwt_client_secret=os.getenv("JWT_CLIENT_SECRET") or "",
    jwt_token_expiration_seconds=int(os.getenv("JWT_TOKEN_EXPIRATION_SECONDS") or "0"),
)


copilot()



