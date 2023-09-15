import json
from typing import List

from langchain.document_loaders import TextLoader
from langchain.schema import Document

from opencopilot.utils.loaders.url_loaders.entities import (
    UnsupportedFileTypeException,
)


def execute(file_name: str, url: str) -> List[Document]:
    if not _is_file_type_json(file_name):
        raise UnsupportedFileTypeException()
    loader = TextLoader(file_name)
    documents = loader.load()
    formatted_documents = []
    for document in documents:
        metadata = document.metadata or {}
        metadata["source"] = url
        formatted_documents.append(
            Document(page_content=document.page_content, metadata=metadata)
        )
    return formatted_documents


def _is_file_type_json(file_name: str) -> bool:
    try:
        with open(file_name, "r") as f:
            content = f.read()
        json.loads(content)
    except:
        return False
    return True
