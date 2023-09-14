from typing import Dict
from typing import List

import trafilatura
from langchain.schema import Document


def execute(file_name: str, url: str) -> List[Document]:
    docs: List[Document] = []
    try:
        with open(file_name, "r") as f:
            content = f.read()
        text = trafilatura.extract(content)
        if not text:
            raise Exception("Failed to extract text")
        metadata: Dict = {
            "source": url,
        }
        extracted_metadata = trafilatura.extract_metadata(content)
        if extracted_metadata and extracted_metadata.title:
            metadata["title"] = extracted_metadata.title
        docs.append(Document(page_content=text, metadata=metadata))
    except Exception as e:
        raise e
    return docs
