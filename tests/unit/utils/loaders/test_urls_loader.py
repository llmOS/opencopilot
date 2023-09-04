from unittest.mock import MagicMock

from opencopilot.src.utils.loaders import urls_loader as loader


class Splitter(MagicMock):
    def split_text(self, content: str):
        return [content]


def setup():
    loader.urllib.request = MagicMock()
    loader.api_logger = MagicMock()


def test_loads_pdf():
    file_name = "tests/assets/urls_loader/sample.pdf"
    url = "https://www.africau.edu/images/default/sample.pdf"
    loader.urllib.request.urlretrieve.return_value = file_name, None
    result = loader.execute([url], Splitter())
    assert len(result) == 2
    assert result[0].metadata["source"] == url
    assert result[1].metadata["page"] == 1
    assert "continued from page 1" in result[1].page_content


def test_loads_csv():
    file_name = "tests/assets/urls_loader/sample.csv"
    url = "https://mock-url.csv"
    loader.urllib.request.urlretrieve.return_value = file_name, None
    result = loader.execute([url], Splitter())
    assert len(result) == 2
    assert result[0].metadata["source"] == url
    assert result[1].metadata["row"] == 1
    assert "Finland" in result[1].page_content


def test_loads_tsv():
    file_name = "tests/assets/urls_loader/sample.tsv"
    url = "https://mock-url.tsv"
    loader.urllib.request.urlretrieve.return_value = file_name, None
    result = loader.execute([url], Splitter())
    assert len(result) == 5
    assert result[0].metadata["source"] == url
    assert result[4].metadata["row"] == 4
    assert "Sepal length: 5.0" in result[4].page_content


def test_loads_xlsx():
    file_name = "tests/assets/urls_loader/sample.xlsx"
    url = "https://mock-url.xlsx"
    loader.urllib.request.urlretrieve.return_value = file_name, None
    result = loader.execute([url], Splitter())
    assert result[0].metadata["source"] == url
    assert "Canada" in result[0].page_content


def test_loads_json():
    file_name = "tests/assets/urls_loader/sample.json"
    url = "https://mock-url.json"
    loader.urllib.request.urlretrieve.return_value = file_name, None
    result = loader.execute([url], Splitter())
    assert result[0].metadata["source"] == url
    assert '"text": "mock text here"' in result[0].page_content


def test_loads_html():
    file_name = "tests/assets/urls_loader/sample.html"
    url = "https://mock-url.html"
    loader.urllib.request.urlretrieve.return_value = file_name, None
    result = loader.execute([url], Splitter())
    assert result[0].metadata["source"] == url
    assert result[0].metadata["title"] == "My epic webpage"
    assert 'Some more content' in result[0].page_content