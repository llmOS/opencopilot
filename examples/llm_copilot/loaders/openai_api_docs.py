from typing import List
from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from langchain.schema import Document
from playwright.sync_api import sync_playwright


def execute(urls: List[str]) -> List[Document]:
    docs: List[Document] = []
    for url in urls:
        soup = _scrape_html_with_playwright(url)
        sections = soup.find_all(class_="section")
        for section in sections:
            urls = section.find_all(class_="anchor-heading-link")
            if len(urls) and urls[0].attrs.get("href"):
                href = urls[0].attrs.get("href")
                docs.append(Document(
                    page_content=section.text,
                    metadata={"source": urljoin(url, href)}
                ))
    return docs


def _scrape_html_with_playwright(url) -> Optional[BeautifulSoup]:
    soup = None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.goto(url)
                page_source = page.content()
                soup = BeautifulSoup(page_source, features="lxml")
            except:
                pass
            browser.close()
    except Exception as e:
        print(e)
    return soup
