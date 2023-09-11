"""
Coding copilot

Prerequisite:
- Before using this module, users need to run CodeLlama LLM:
    opencopilot run codellama-[7, 13, 34]b

Key Components:
- OpenCopilot: Main class for setting up the Opencopilot.
- LocalLLM: A local instance of the language model used for code generation.
- HuggingFaceEmbeddings: Used for generating embeddings based on a model from the HuggingFace model hub.
- PROMPT: The template used by OpenCopilot for generating code based on given coding questions.

Environment Variables:
- HOST: The host URL for the OpenCopilot service.
- AUTH_TYPE: The authentication method used for the service.
- JWT_CLIENT_ID and JWT_CLIENT_SECRET: Credentials for JWT authentication.
- JWT_TOKEN_EXPIRATION_SECONDS: Expiration time for JWT tokens.

Usage:
Simply run and use `opencopilot chat` CLI to query the code copilot.
"""

from langchain.embeddings import HuggingFaceEmbeddings

from opencopilot import OpenCopilot
from opencopilot.domain.chat.models import LocalLLM


PROMPT = """<s>[INST] <<SYS>>
Write code to solve the following coding problem that obeys the constraints and passes the example test cases. 
Please wrap your code answer using ```.
Relevant information: {context}. 
<</SYS>>

{history} {question} [/INST]
"""

llm = LocalLLM(
    temperature=0.7,
    llm_url="http://127.0.0.1:8000/",
)

embeddings = HuggingFaceEmbeddings(model_name="thenlper/gte-base")

copilot = OpenCopilot(
    prompt=PROMPT,
    question_template=" {question} [/INST] ",
    response_template="{response} </s><s> [INST]",
    copilot_name="codellama_copilot",
    llm=llm,
    embedding_model=embeddings,
)


copilot()
