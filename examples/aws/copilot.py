from bs4 import BeautifulSoup
from typing import List
import requests
from langchain.schema import Document

from opencopilot import OpenCopilot

copilot = OpenCopilot(
    prompt_file="prompt_template.txt",
    copilot_name="AWS",
)

copilot.add_data_urls([
    "https://awsdocs.s3.amazonaws.com/cli/latest/aws-cli.pdf",
])


@copilot.data_loader
def load_aws_cli_reference_links() -> List[Document]:
    url = "https://awscli.amazonaws.com/v2/documentation/api/latest/index.html"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features="lxml")
        text = _get_page_text(soup)
        formatted_links = _get_reference_links(soup, url)
        return [Document(
            page_content=text + " " + " ".join(formatted_links),
            metadata={"source": url}
        )]
    except:
        print("Failed to get AWS CLI command reference links")
        return []


def _get_page_text(soup):
    title = soup.find_all("h1")[0].text
    subtitle = soup.find_all("div", class_="section")[0].find_all("p")[0].text
    return f"{title} {subtitle}"


def _get_reference_links(soup, url):
    links = soup.find_all("a", class_="reference internal")
    formatted_links = []
    for link in links:
        formatted_links.append(url.replace("index.html", link.attrs["href"]))
    return formatted_links


copilot()
