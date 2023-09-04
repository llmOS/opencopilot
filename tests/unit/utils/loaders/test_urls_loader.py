from unittest.mock import MagicMock

from filetype import Type

from opencopilot.src.utils.loaders import urls_loader as loader


def setup():
    loader.urllib.request = MagicMock()
    loader.split_documents_use_case = MagicMock()
    loader.html_loader_use_case = MagicMock()
    loader.pdf_loader_use_case = MagicMock()
    loader.filetype = MagicMock()


def test_detects_pdf():
    file_name = "mock_file_name"
    url = "some-url.pdf"
    loader.urllib.request.urlretrieve.return_value = file_name, None
    loader.filetype.guess.return_value = Type(
        mime="application/pdf",
        extension="pdf"
    )
    loader.execute([url], MagicMock())
    loader.pdf_loader_use_case.execute.assert_called_with(
        file_name, url
    )


def test_uses_html_as_fallback():
    file_name = "mock_file_name"
    url = "some-url.com"
    loader.urllib.request.urlretrieve.return_value = file_name, None
    loader.filetype.guess.return_value = None
    loader.execute([url], MagicMock())
    loader.html_loader_use_case.execute.assert_called_with(
        file_name, url
    )
