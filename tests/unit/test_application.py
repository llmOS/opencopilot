import os
from unittest.mock import MagicMock

import pytest

from opencopilot import settings
from opencopilot import application
from opencopilot.application import OpenCopilot
from opencopilot.domain.errors import APIKeyError
from opencopilot.domain.errors import ModelError
from opencopilot.domain.errors import PromptError

# API key
MOCK_OPENAI_API_KEY = "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"
LLM_MODEL_NAME = "gpt-3.5-turbo-16k"
VALID_PROMPT_FILE = "tests/assets/prompts/valid_prompt.txt"
NO_USER_QUESTION_PROMPT_FILE = "tests/assets/prompts/no_user_question.txt"


def setup_function():
    os.environ["OPENAI_API_KEY"] = ""
    settings._settings = None


def test_valid():
    OpenCopilot(
        prompt_file=VALID_PROMPT_FILE,
        openai_api_key=MOCK_OPENAI_API_KEY,
    )


def test_openai_api_key_empty():
    with pytest.raises(APIKeyError):
        OpenCopilot(
            openai_api_key="",
            prompt_file=VALID_PROMPT_FILE,
        )


def test_openai_api_key_bad_format():
    with pytest.raises(APIKeyError):
        OpenCopilot(
            openai_api_key="this is a misformatted OpenAI API key",
            prompt_file=VALID_PROMPT_FILE,
        )


def test_prompt_file_missing():
    with pytest.raises(PromptError):
        OpenCopilot(
            prompt_file="this file definitely should not exist.mikrofilm",
            openai_api_key=MOCK_OPENAI_API_KEY,
        )


def test_prompt_file_invalid():
    with pytest.raises(PromptError):
        OpenCopilot(
            prompt_file=NO_USER_QUESTION_PROMPT_FILE,
            openai_api_key=MOCK_OPENAI_API_KEY,
        )


def test_prompt_string_valid():
    OpenCopilot(
        prompt=open(VALID_PROMPT_FILE, "r").read(),
        openai_api_key=MOCK_OPENAI_API_KEY,
    )


def test_prompt_string_invalid():
    with pytest.raises(PromptError):
        OpenCopilot(
            prompt=open(NO_USER_QUESTION_PROMPT_FILE, "r").read(),
            openai_api_key=MOCK_OPENAI_API_KEY,
        )


def test_no_prompt_string_or_file_present():
    with pytest.raises(PromptError):
        OpenCopilot(
            openai_api_key=MOCK_OPENAI_API_KEY,
        )


def test_both_prompt_string_and_file_present():
    with pytest.raises(PromptError):
        OpenCopilot(
            prompt=open(VALID_PROMPT_FILE, "r").read(),
            prompt_file=VALID_PROMPT_FILE,
            openai_api_key=MOCK_OPENAI_API_KEY,
        )


def test_invalid_model_name():
    with pytest.raises(ModelError):
        OpenCopilot(
            prompt_file=VALID_PROMPT_FILE,
            openai_api_key=MOCK_OPENAI_API_KEY,
            llm_model_name="invalid"
        )


def test_sets_log_level():
    application.api_logger = MagicMock()
    OpenCopilot(
        prompt_file=VALID_PROMPT_FILE,
        openai_api_key=MOCK_OPENAI_API_KEY,
        log_level="log_level"
    )
    application.api_logger.set_log_level.assert_called_with("log_level")
