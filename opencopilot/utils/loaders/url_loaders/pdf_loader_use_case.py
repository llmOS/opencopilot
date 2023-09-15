from typing import List

from filetype import filetype
from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document

from opencopilot.utils.loaders.url_loaders.entities import (
    UnsupportedFileTypeException,
)


def execute(file_name: str, url: str) -> List[Document]:
    if not _is_file_type_pdf(file_name):
        raise UnsupportedFileTypeException()
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


def _is_file_type_pdf(file_name: str) -> bool:
    mime_type: str = ""
    try:
        kind = filetype.guess(file_name)
        mime_type = kind.mime
    except:
        pass
    return mime_type == "application/pdf"
