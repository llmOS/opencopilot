"""
LLM copilot

Prerequisite:
- Before using this module, users need to run the LLM:
    opencopilot run llama-[7, 13, 34]b-chat

Key Components:
- OpenCopilot: Main class for setting up the Opencopilot.
- LocalLLM: A local instance of the language model used for code generation.
- HuggingFaceEmbeddings: Used for generating embeddings based on a model from the HuggingFace model hub.
- PROMPT: The template used by OpenCopilot for answering AI-related questions.
cd 
Environment Variables:
- HOST: The host URL for the OpenCopilot service.
- AUTH_TYPE: The authentication method used for the service.
- HELICONE_API_KEY: API key for the Helicone service.
- JWT_CLIENT_ID and JWT_CLIENT_SECRET: Credentials for JWT authentication.
- JWT_TOKEN_EXPIRATION_SECONDS: Expiration time for JWT tokens.

Usage:
Simply run and use `opencopilot chat` CLI to query the LLM copilot.
"""

import os
from typing import List
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.document_loaders.sitemap import SitemapLoader

from opencopilot import OpenCopilot

load_dotenv()

copilot = OpenCopilot(
    prompt_file="prompt_template.txt",
    copilot_name="llm",
    weaviate_url=os.getenv("WEAVIATE_URL"),
    helicone_api_key=os.getenv("HELICONE_API_KEY"),
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
        filter_urls=["https://weaviate.io/developers/weaviate"],
    )
    documents = loader.load()
    return documents


copilot()
