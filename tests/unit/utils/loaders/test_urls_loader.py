from unittest.mock import MagicMock
from unittest.mock import patch

from opencopilot.utils.loaders import urls_loader as loader


class Splitter(MagicMock):
    def split_text(self, content: str):
        return [content]


def setup():
    loader.requests = MagicMock()
    loader.requests.return_value = MagicMock()
    loader.api_logger = MagicMock()
    loader.tempfile = MagicMock()


def _set_tempfile(file_name: str, mock_module):
    # file = MagicMock()
    mock_module.name = file_name
    mock_module.__enter__.return_value = mock_module
    loader.tempfile.NamedTemporaryFile.return_value = mock_module


def test_loads_pdf():
    url = "https://www.africau.edu/images/default/sample.pdf"
    file_name = "tests/assets/urls_loader/sample.pdf"
    with patch("opencopilot.utils.loaders.urls_loader.tempfile") as mock_module:
        _set_tempfile(file_name, mock_module)
        result = loader.execute([url], Splitter(), 50)
        assert len(result) == 2
        assert result[0].metadata["source"] == url
        assert result[1].metadata["page"] == 1
        assert "continued from page 1" in result[1].page_content


def test_loads_csv():
    url = "https://mock-url.csv"
    file_name = "tests/assets/urls_loader/sample.csv"
    with patch("opencopilot.utils.loaders.urls_loader.tempfile") as mock_module:
        _set_tempfile(file_name, mock_module)
        result = loader.execute([url], Splitter(), 50)
        assert len(result) == 2
        assert result[0].metadata["source"] == url
        assert result[1].metadata["row"] == 1
        assert "Finland" in result[1].page_content


def test_loads_tsv():
    url = "https://mock-url.tsv"
    file_name = "tests/assets/urls_loader/sample.tsv"
    with patch("opencopilot.utils.loaders.urls_loader.tempfile") as mock_module:
        _set_tempfile(file_name, mock_module)
        result = loader.execute([url], Splitter(), 50)
        assert len(result) == 5
        assert result[0].metadata["source"] == url
        assert result[4].metadata["row"] == 4
        assert "Sepal length: 5.0" in result[4].page_content


def test_loads_xlsx():
    url = "https://mock-url.xlsx"
    file_name = "tests/assets/urls_loader/sample.xlsx"
    with patch("opencopilot.utils.loaders.urls_loader.tempfile") as mock_module:
        _set_tempfile(file_name, mock_module)
        result = loader.execute([url], Splitter(), 50)
        assert result[0].metadata["source"] == url
        assert "Canada" in result[0].page_content


def test_loads_json():
    url = "https://mock-url.json"
    file_name = "tests/assets/urls_loader/sample.json"
    with patch("opencopilot.utils.loaders.urls_loader.tempfile") as mock_module:
        _set_tempfile(file_name, mock_module)
        result = loader.execute([url], Splitter(), 50)
        assert result[0].metadata["source"] == url
        assert '"text": "mock text here"' in result[0].page_content


def test_loads_html():
    url = "https://mock-url.html"
    file_name = "tests/assets/urls_loader/sample.html"
    with patch("opencopilot.utils.loaders.urls_loader.tempfile") as mock_module:
        _set_tempfile(file_name, mock_module)
        result = loader.execute([url], Splitter(), 50)
        assert result[0].metadata["source"] == url
        assert result[0].metadata["title"] == "My epic webpage"
        assert 'Some more content' in result[0].page_content
