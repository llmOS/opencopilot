import time
from typing import List
from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from langchain.schema import Document
from playwright.sync_api import sync_playwright


def execute(urls: List[str]) -> List[Document]:
    main_urls = _get_main_urls(urls)
    main_urls = list(set(main_urls))
    docs = _scrape_url_contents(main_urls)
    return docs


def _get_main_urls(urls: List[str]) -> List[str]:
    links: List[str] = []
    for url in urls:
        soup = _scrape_html_with_playwright(url)
        if soup:
            new_links = _find_links(soup, url)
            links += new_links
    return links


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


def _find_links(
        soup: BeautifulSoup,
        base_url: str,
) -> List[str]:
    links: List[str] = []
    tags = soup.find_all("a", class_="nx-flex")
    for tag in tags:
        if href := tag.attrs.get("href"):
            links.append(urljoin(base_url, href))
    return links


def _scrape_url_contents(all_urls: List[str]) -> List[Document]:
    docs: List[Document] = []
    count = 0
    for url in all_urls:
        soup = _scrape_html_with_playwright(url)
        tags = soup.find_all("main", class_="nx-w-full")
        if len(tags):
            docs.append(Document(
                page_content=tags[0].text,
                metadata={
                    "source": url,
                }
            ))
        else:
            print(f"Failed for url: {url}")
        time.sleep(1.5)
        count += 1
        if count % 10 == 0:
            print(f"{count}/{len(all_urls)}")
    return docs
