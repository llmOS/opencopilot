from typing import List
from typing import Optional
from langchain.schema import BaseMessage
from opencopilot.repository.documents.document_store import DocumentStore

from opencopilot import OpenCopilot

copilot = OpenCopilot(
    copilot_name="AWS CLI Copilot",
    llm="gpt-3.5-turbo-16k", # You can also use gpt-4 for improved accuracy
    prompt_file="prompt_template.txt"
)

@copilot.prompt_builder
def builder(message: str, history: List[BaseMessage], document_store: DocumentStore) -> Optional[str]:
    return "Do the chacha"

# Download and embed the knowledge base from given URL
copilot.add_data_urls([
    "https://awsdocs.s3.amazonaws.com/cli/latest/aws-cli.pdf",
])

# Run the copilot
copilot()
