import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import Callable
from typing import List

from langchain.schema import Document

import loaders.anthropic_docs as anthropic_docs_loader
import loaders.openai_docs as openai_docs_loader
import loaders.openai_docs as openai_docs_loader
import loaders.url as url_loader
import loaders.prompting_guide_docs as prompting_guide_docs_loader
import loaders.fullstack_deeplearning as fullstack_deeplearning_loader

LOADERS_MAP = {
    "openai_docs": openai_docs_loader.execute,
    "openai_api_docs": openai_docs_loader.execute,
    "anthropic_docs": anthropic_docs_loader.execute,
    "url": url_loader.execute,
    "prompting_guide_docs": prompting_guide_docs_loader.execute,
    "fullstack_deeplearning": fullstack_deeplearning_loader.execute
}


class SourceType(Enum):
    OPENAI_DOCS = "openai_docs"
    OPENAI_API_DOCS = "openai_api_docs"
    ANTHROPIC_DOCS = "anthropic_docs"
    URL = "url"
    PROMPTING_GUIDE_DOCS = "prompting_guide_docs"
    FULLSTACK_DEEPLEARNING = "fullstack_deeplearning"


@dataclass
class DataLoader:
    source_type: SourceType
    sources: List[str]
    destination_file: str  # myfile.json


def execute(data_loaders: List[DataLoader]):
    for data_loader in data_loaders:
        if loader := LOADERS_MAP.get(data_loader.source_type.value):
            _scrape(
                file_dump_path=data_loader.destination_file,
                loader_function=loader,
                urls=data_loader.sources,
            )


def _scrape(
        file_dump_path: str,
        loader_function: Callable[[List[str]], List[Document]],
        urls: List[str],
) -> None:
    if not os.path.exists(file_dump_path):
        scraped_documents = loader_function(urls)

        json_docs = [d.json() for d in scraped_documents]
        formatted_docs = [json.loads(d) for d in json_docs]

        file_dump_dir = os.path.dirname(file_dump_path)
        if file_dump_dir:
            os.makedirs(file_dump_dir, exist_ok=True)
        with open(file_dump_path, "w") as f:
            f.write(json.dumps(formatted_docs, indent=4))
