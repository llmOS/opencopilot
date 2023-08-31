import pytest

from opencopilot.application import OpenCopilot
from opencopilot.domain.errors import APIKeyError, ModelError, PromptError


# API key
MOCK_OPENAI_API_KEY = "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"
LLM_MODEL_NAME = "gpt-3.5-turbo-16k"
VALID_PROMPT_FILE = "tests/assets/prompts/valid_prompt.txt"
NO_USER_QUESTION_PROMPT_FILE = "tests/assets/prompts/no_user_question.txt"


def test_openai_api_key_empty():
    with pytest.raises(APIKeyError):
        copilot = OpenCopilot(
            openai_api_key="",
            prompt_file=VALID_PROMPT_FILE,
        )

def test_openai_api_key_bad_format():
    with pytest.raises(APIKeyError):
        copilot = OpenCopilot(
            openai_api_key="this is a misformatted OpenAI API key",
            prompt_file=VALID_PROMPT_FILE,
        )


def test_prompt_file_missing():
    with pytest.raises(PromptError):
        copilot = OpenCopilot(
            prompt_file="this file definitely should not exist.mikrofilm",
            openai_api_key=MOCK_OPENAI_API_KEY,
        )


def test_prompt_file_valid():
    copilot = OpenCopilot(
        prompt_file=VALID_PROMPT_FILE,
        openai_api_key=MOCK_OPENAI_API_KEY,
    )


def test_prompt_file_invalid():
    with pytest.raises(PromptError):
        copilot = OpenCopilot(
            prompt_file=NO_USER_QUESTION_PROMPT_FILE,
            openai_api_key=MOCK_OPENAI_API_KEY,
        )

def test_prompt_string_valid():
    copilot = OpenCopilot(
        prompt=open(VALID_PROMPT_FILE, "r").read(),
        openai_api_key=MOCK_OPENAI_API_KEY,
    )


def test_prompt_string_invalid():
    with pytest.raises(PromptError):
        copilot = OpenCopilot(
            prompt=open(NO_USER_QUESTION_PROMPT_FILE, "r").read(),
            openai_api_key=MOCK_OPENAI_API_KEY,
        )


def test_no_prompt_string_or_file_present():
    with pytest.raises(PromptError):
        copilot = OpenCopilot(
            openai_api_key=MOCK_OPENAI_API_KEY,
        )

def test_both_prompt_string_and_file_present():
    with pytest.raises(PromptError):
        copilot = OpenCopilot(
            prompt=open(VALID_PROMPT_FILE, "r").read(),
            prompt_file=VALID_PROMPT_FILE,
            openai_api_key=MOCK_OPENAI_API_KEY,
        )
