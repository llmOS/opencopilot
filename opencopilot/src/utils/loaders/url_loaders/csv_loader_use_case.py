import csv
from typing import List

from langchain.document_loaders import CSVLoader
from langchain.schema import Document


def execute(file_name: str, url: str) -> List[Document]:
    with open(file_name, newline="") as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
    loader = CSVLoader(
        file_path=file_name,
        csv_args={
            "delimiter": dialect.delimiter,
        },
    )
    documents = loader.load()
    formatted_documents = []
    for document in documents:
        metadata = document.metadata or {}
        metadata["source"] = url
        formatted_documents.append(
            Document(page_content=document.page_content, metadata=metadata)
        )
    return formatted_documents
