from typing import Dict
from typing import List
from typing import Optional

import trafilatura
from langchain.schema import Document
from langchain.text_splitter import TextSplitter

from opencopilot.logger import api_logger
from opencopilot.repository.documents import split_documents_use_case

logger = api_logger.get()


def execute(urls: List[str], text_splitter: TextSplitter) -> List[Document]:
    documents: List[Document] = []
    for url in urls:
        scraped_document = _scrape_html(url)
        if scraped_document:
            documents.append(scraped_document)
    return split_documents_use_case.execute(text_splitter, documents)


def _scrape_html(url) -> Optional[Document]:
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            raise Exception()
        text = trafilatura.extract(downloaded)
        if not text:
            raise Exception("Failed to extract text")
        metadata: Dict = {
            "source": url,
        }
        extracted_metadata = trafilatura.extract_metadata(downloaded)
        if extracted_metadata and extracted_metadata.title:
            metadata["title"] = extracted_metadata.title
        return Document(page_content=text, metadata=metadata)
    except Exception as e:
        logger.warning(f"Failed to scrape the contents from {url}")
