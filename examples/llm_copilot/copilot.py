import os
from typing import List
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.document_loaders.sitemap import SitemapLoader

from opencopilot import OpenCopilot

load_dotenv()

copilot = OpenCopilot(
    prompt_file="prompts/prompt_template.txt",
    copilot_name="llm",
    host=os.getenv("HOST"),
    auth_type=os.getenv("AUTH_TYPE"),
    weaviate_url=os.getenv("WEAVIATE_URL"),
    helicone_api_key=os.getenv("HELICONE_API_KEY"),
    jwt_client_id=os.getenv("JWT_CLIENT_ID") or "",
    jwt_client_secret=os.getenv("JWT_CLIENT_SECRET") or "",
    jwt_token_expiration_seconds=int(os.getenv("JWT_TOKEN_EXPIRATION_SECONDS") or "0")
)
copilot.add_local_files_dir("data")

@copilot.data_loader
def load_opencopilot_docs() -> List[Document]:
    loader = SitemapLoader("https://docs.opencopilot.dev/sitemap.xml")
    documents = loader.load()
    return documents

@copilot.data_loader
def load_helicone_docs() -> List[Document]:
    loader = SitemapLoader("https://docs.helicone.ai/sitemap.xml")
    documents = loader.load()
    return documents


@copilot.data_loader
def load_weaviate_docs() -> List[Document]:
    loader = SitemapLoader(
        "https://weaviate.io/sitemap.xml",
        filter_urls=[
            "https://weaviate.io/developers/weaviate"
        ]
    )
    documents = loader.load()
    return documents

copilot()
