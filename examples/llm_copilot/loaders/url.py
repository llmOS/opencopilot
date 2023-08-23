from typing import List

from langchain.document_loaders import PlaywrightURLLoader
from langchain.document_loaders import UnstructuredURLLoader
from langchain.schema import Document


def execute(urls: List[str]) -> List[Document]:
    documents: List[Document] = []
    for url in urls:
        scraped_documents = _scrape_webpage(url)
        documents.extend(scraped_documents)
    return documents


def _scrape_webpage(url) -> List[Document]:
    documents = _scrape_html(url)
    if not documents or len(documents) == 1 and len(documents[0].page_content) < 20:
        documents = _scrape_html_with_playwright(url)
    return documents


def _scrape_html(url) -> List[Document]:
    try:
        loader = UnstructuredURLLoader(urls=[url])
        return loader.load()
    except:
        return []


def _scrape_html_with_playwright(url) -> List[Document]:
    try:
        loader = PlaywrightURLLoader(
            urls=[url],
            remove_selectors=["header", "footer"]
        )
        return loader.load()
    except Exception as e:
        print(e)
    return []
