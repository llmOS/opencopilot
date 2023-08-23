import time
from typing import List
from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from langchain.schema import Document
from playwright.sync_api import sync_playwright


def execute(urls: List[str]) -> List[Document]:
    print("Scraping anthropic docs..")
    main_urls = _get_all_urls(urls)
    main_urls = list(set(main_urls))
    docs: List[Document] = []
    for url in main_urls:
        soup = _scrape_html_with_playwright(url)
        tags = soup.find_all(class_="rm-Article")
        if len(tags):
            docs.append(Document(
                page_content=tags[0].text,
                metadata={"source": url}
            ))
        time.sleep(0.3)
    print("Scraped anthropic docs..")
    return docs


def _get_all_urls(urls: List[str]) -> List[str]:
    all_urls = []
    for url in urls:
        soup = _scrape_html_with_playwright(url)
        tags = soup.find_all("a", class_="rm-Sidebar-link")
        for tag in tags:
            if classes := tag.attrs.get("class"):
                if "side-nav-child" not in classes:
                    if href := tag.attrs.get("href"):
                        all_urls.append(urljoin(url, href))
    return all_urls


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
