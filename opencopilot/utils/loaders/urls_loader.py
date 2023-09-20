import tempfile
from typing import Callable
from typing import List

import requests
from langchain.schema import Document
from langchain.text_splitter import TextSplitter
from requests import Response

from opencopilot.domain.errors import FileSizeExceededError
from opencopilot.logger import api_logger
from opencopilot.repository.documents import split_documents_use_case
from opencopilot.utils.loaders.url_loaders import csv_loader_use_case
from opencopilot.utils.loaders.url_loaders import html_loader_use_case
from opencopilot.utils.loaders.url_loaders import json_loader_use_case
from opencopilot.utils.loaders.url_loaders import pdf_loader_use_case
from opencopilot.utils.loaders.url_loaders import xls_loader_use_case

logger = api_logger.get()

LOADERS: List[Callable[[str, str], List[Document]]] = [
    pdf_loader_use_case.execute,
    csv_loader_use_case.execute,
    xls_loader_use_case.execute,
    json_loader_use_case.execute,
    html_loader_use_case.execute,
]

USER_AGENT: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0"
CHUNK_SIZE = 5 * 1024 * 1024  # 5MB


def execute(
    urls: List[str], text_splitter: TextSplitter, max_document_size_mb: int
) -> List[Document]:
    documents: List[Document] = []
    success_count: int = 0
    for url in urls:
        new_docs = _load_url(url, max_document_size_mb)
        documents.extend(new_docs)
        if new_docs:
            success_count += 1
    logger.info(f"Successfully scraped {success_count} url{'s'[:success_count ^ 1]}.")
    return split_documents_use_case.execute(text_splitter, documents)


def _load_url(url: str, max_document_size_mb: int) -> List[Document]:
    docs: List[Document] = []
    try:
        response = requests.get(url, stream=True, headers={"User-agent": USER_AGENT})
        response.raise_for_status()

        with tempfile.NamedTemporaryFile() as temp_file:
            file_name: str = _download_webpage(
                response, temp_file, max_document_size_mb
            )
            docs.extend(_load_docs_from_file(file_name, url))
    except FileSizeExceededError as e:
        logger.warning(f"Document {url} too big, skipping.")
        return []
    except Exception as e:
        logger.warning(f"Failed to scrape the contents from {url}")
        return []
    return docs


def _download_webpage(
    response: Response,
    temp_file: tempfile.NamedTemporaryFile,
    max_document_size_mb: int,
) -> str:
    downloaded_size = 0
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        downloaded_size += len(chunk)
        if downloaded_size > max_document_size_mb * 1024 * 1024:
            raise FileSizeExceededError("")
        temp_file.write(chunk)
    temp_file.flush()
    return temp_file.name


def _load_docs_from_file(file_name: str, url: str) -> List[Document]:
    docs = []
    for loader in LOADERS:
        try:
            new_docs = loader(file_name, url)
            if new_docs:
                docs.extend(new_docs)
                break
        except Exception as e:
            pass
    return docs
