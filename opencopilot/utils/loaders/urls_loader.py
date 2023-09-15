import os
import urllib.request
from typing import Callable
from typing import List

from langchain.schema import Document
from langchain.text_splitter import TextSplitter

from opencopilot import settings
from opencopilot.logger import api_logger
from opencopilot.repository.documents import split_documents_use_case
from opencopilot.utils.loaders.url_loaders import csv_loader_use_case
from opencopilot.utils.loaders.url_loaders import html_loader_use_case
from opencopilot.utils.loaders.url_loaders import json_loader_use_case
from opencopilot.utils.loaders.url_loaders import pdf_loader_use_case
from opencopilot.utils.loaders.url_loaders import xls_loader_use_case

logger = api_logger.get()

loaders: List[Callable[[str, str], List[Document]]] = [
    pdf_loader_use_case.execute,
    csv_loader_use_case.execute,
    xls_loader_use_case.execute,
    json_loader_use_case.execute,
    html_loader_use_case.execute,
]


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
        file_name, headers = urllib.request.urlretrieve(url)
        if (file_size := _get_file_size(file_name)) > max_document_size_mb:
            logger.warning(
                f"Document {url} too big ({file_size} > {settings.get().MAX_DOCUMENT_SIZE_MB}), skipping."
            )
            return []
        for loader in loaders:
            try:
                new_docs = loader(file_name, url)
                if new_docs:
                    docs.extend(new_docs)
                    break
            except Exception as e:
                pass
    except Exception as e:
        pass
    if not docs:
        logger.warning(f"Failed to scrape the contents from {url}")
    return docs


def _get_file_size(file_path):
    size_in_bytes = os.path.getsize(file_path)
    size_in_mb = size_in_bytes / 1024 / 1024
    return size_in_mb
