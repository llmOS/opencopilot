import os
from typing import List

from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

from opencopilot import OpenCopilot
from opencopilot.domain.chat.models.local import LocalLLM

load_dotenv()

PROMPT = """<s>[INST] <<SYS>>
Your purpose is to repeat what the user says, but in a different wording.
Don't add anything, don't answer any questions, don't give any advice or comment - just repeat.
Context:
{context}
<</SYS>>

{history} Repeat: {question} [/INST]
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
    copilot_name="oss_copilot",
    llm=llm,
    embedding_model=embeddings,
    weaviate_url=os.getenv("WEAVIATE_URL"),
)


@copilot.data_loader
def load_opencopilot_docs() -> List[Document]:
    return [
        Document(
            page_content="OpenCopilot allows you to build your copilot in a single day",
            metadata={"source": "github"}
        )
    ]


copilot()
