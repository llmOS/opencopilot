from typing import List

from langchain.schema import Document
from langchain.text_splitter import TextSplitter


def execute(text_splitter: TextSplitter, documents: List[Document]) -> List[Document]:
    document_chunks = []
    for document in documents:
        for chunk in text_splitter.split_text(document.page_content):
            document_chunks.append(
                Document(page_content=chunk, metadata=document.metadata)
            )
    return document_chunks
