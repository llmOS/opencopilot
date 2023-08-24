import csv
import json
import os
import re
from typing import List

from langchain.document_loaders import CSVLoader
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import UnstructuredExcelLoader
from langchain.document_loaders import UnstructuredFileLoader
from langchain.schema import Document

from opencopilot import settings


def execute(
    data_dir: str, is_loading_deprecated=False, text_splitter=None
) -> List[Document]:
    files = []
    if not data_dir or not os.path.isdir(data_dir):
        return []
    ignore_files = [".DS_Store"]
    for dir_path, dir_names, file_names in os.walk(data_dir):
        for file_name in file_names:
            if file_name not in ignore_files:
                files.append(os.path.join(dir_path, file_name))

    files_count = len(files)
    if files_count > 0:
        print(f"[Loading {files_count} file{'s'[:files_count ^ 1]} from {data_dir}.]")
    else:
        raise Exception(f"[Add files to {data_dir}.]")

    documents = []
    for file_path in files:
        new_documents = []
        if (
            file_size := _get_file_size(file_path)
        ) > settings.get().MAX_DOCUMENT_SIZE_MB:
            print(
                f"Document {file_path} too big ({file_size} > {settings.get().MAX_DOCUMENT_SIZE_MB}), skipping."
            )
            continue
        if file_path.endswith(".csv"):
            with open(file_path, newline="") as csvfile:
                dialect = csv.Sniffer().sniff(csvfile.read(1024))

            loader = CSVLoader(
                file_path=file_path,
                csv_args={
                    "delimiter": dialect.delimiter,
                },
            )
            new_documents = loader.load()
        elif file_path.endswith(".tsv"):
            loader = CSVLoader(
                file_path=file_path,
                csv_args={
                    "delimiter": "\t",
                },
            )
            new_documents = loader.load()
        elif file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            new_documents = loader.load()
        elif file_path.endswith(".xls") or file_path.endswith(".xlsx"):
            loader = UnstructuredExcelLoader(file_path)
            new_documents = loader.load()
        elif file_path.endswith(".json") and os.path.basename(file_path).startswith(
            "serialized_documents_"
        ):
            with open(file_path, "r") as f:
                document_dicts = json.load(f)
            for document in document_dicts:
                metadata = document["metadata"]
                if metadata["source"] in settings.get().copilot_config.data.get(
                    "ignore", []
                ):
                    continue
                if "deprecated" in metadata["source"]:
                    if not is_loading_deprecated:
                        # skip deprecated information
                        continue
                    document["metadata"]["deprecated"] = True
                content = _cleanup_document(document["page_content"])
                new_documents.append(Document(page_content=content, metadata=metadata))
        elif file_path.endswith(".json"):
            loader = TextLoader(file_path)
            new_documents = loader.load()
        else:
            try:
                loader = UnstructuredFileLoader(file_path)
                new_documents = loader.load()
            except Exception as e:
                print(f"Error loading {file_path}")
        if text_splitter:
            document_chunks = []
            for document in new_documents:
                for chunk in text_splitter.split_text(document.page_content):
                    document_chunks.append(
                        Document(page_content=chunk, metadata=document.metadata)
                    )
            print(
                f"Generated {len(document_chunks)} document chunks from {len(new_documents)} documents"
            )
            documents.extend(document_chunks)
        else:
            print(f"Generated {len(new_documents)} documents")
            documents.extend(new_documents)
    return documents


def _cleanup_document(text: str) -> str:
    # cleanup special unicode characters + trailing newline
    pattern = r"[\u00A0-\uFFFF]\n?"
    clean = re.sub(pattern, "", text)
    clean = re.sub("\n+", "\n", clean)
    return clean


def _get_file_size(file_path):
    size_in_bytes = os.path.getsize(file_path)
    size_in_mb = size_in_bytes / 1024 / 1024
    return size_in_mb
