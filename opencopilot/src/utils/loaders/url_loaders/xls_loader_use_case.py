from typing import List

from langchain.document_loaders import UnstructuredExcelLoader
from langchain.schema import Document


def execute(file_name: str, url: str) -> List[Document]:
    loader = UnstructuredExcelLoader(file_name)
    documents = loader.load()
    formatted_documents = []
    for document in documents:
        metadata = document.metadata or {}
        metadata["source"] = url
        formatted_documents.append(
            Document(page_content=document.page_content, metadata=metadata)
        )
    return formatted_documents
