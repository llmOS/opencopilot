import urllib.request
from typing import List
from typing import Optional

import filetype
from langchain.schema import Document
from langchain.text_splitter import TextSplitter

from opencopilot.logger import api_logger
from opencopilot.repository.documents import split_documents_use_case
from opencopilot.src.utils.loaders.url_loaders import html_loader_use_case
from opencopilot.src.utils.loaders.url_loaders import pdf_loader_use_case

logger = api_logger.get()


def execute(urls: List[str], text_splitter: TextSplitter) -> List[Document]:
    documents: List[Document] = []
    for url in urls:
        documents.extend(_scrape_html(url))
    return split_documents_use_case.execute(text_splitter, documents)


def _scrape_html(url: str) -> List[Document]:
    docs: List[Document] = []
    try:
        file_name, headers = urllib.request.urlretrieve(url)
        file_type = _get_file_type(file_name)
        if file_type == "application/pdf":
            docs.extend(pdf_loader_use_case.execute(file_name, url))
        else:
            docs.extend(html_loader_use_case.execute(file_name, url))
    except:
        logger.warning(f"Failed to scrape the contents from {url}")
    return docs


def _get_file_type(file_name: str) -> Optional[str]:
    kind = None
    try:
        kind = filetype.guess(file_name)
    except:
        pass
    return kind.mime if kind else None
