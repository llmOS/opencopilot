from langchain.embeddings import HuggingFaceEmbeddings

from opencopilot import OpenCopilot
from opencopilot.domain.chat.models.local import LocalLLM


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
