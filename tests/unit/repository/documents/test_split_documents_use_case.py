from unittest.mock import MagicMock

from langchain.schema import Document

from opencopilot.repository.documents import split_documents_use_case as use_case


def _get_text_splitter():
    splitter = MagicMock()
    splitter.split_text.return_value = ["1", "2"]
    return splitter


def setup():
    pass


def test_success_maintains_metadata():
    metadata = {
        "source": "mock-source",
        "title": "mock-title",
        "random": "random-value",
    }
    documents = [
        Document(
            page_content="12",
            metadata={
                "source": "mock-source",
                "title": "mock-title",
                "random": "random-value",
            }
        )
    ]
    result = use_case.execute(_get_text_splitter(), documents)
    assert result == [
        Document(
            page_content="1",
            metadata=metadata,
        ),
        Document(
            page_content="2",
            metadata=metadata,
        ),
    ]
