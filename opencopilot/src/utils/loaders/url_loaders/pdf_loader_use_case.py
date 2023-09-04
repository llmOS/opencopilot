from typing import List

from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document


def execute(file_name: str, url: str) -> List[Document]:
    formatted_docs = []
    loader = PyPDFLoader(file_name)
    docs = loader.load()
    for doc in docs:
        formatted_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": url, "page": doc.metadata.get("page")},
            )
        )
    return formatted_docs
