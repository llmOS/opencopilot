import pytest

from opencopilot.application import OpenCopilot
from opencopilot.domain.errors import APIKeyError, ModelError, PromptError


# API key
LLM_MODEL_NAME = "gpt-3.5-turbo-16k"
VALID_PROMPT_FILE = "tests/assets/prompts/minimal_prompt.txt"


def test_openai_api_key_empty():
    with pytest.raises(APIKeyError):
        copilot = OpenCopilot(
            openai_api_key="",
            prompt_file=VALID_PROMPT_FILE,
        )

def test_openai_api_key_malformed():
    with pytest.raises(APIKeyError):
        copilot = OpenCopilot(
            openai_api_key="this is a misformatted OpenAI API key",
            prompt_file=VALID_PROMPT_FILE,
        )


def test_model_name_invalid():
    with pytest.raises(ModelError):
        copilot = OpenCopilot(
            llm_model_name="gpt-not-a-valid-model-name",
            prompt_file=VALID_PROMPT_FILE,
        )


def test_openai_api_key_rejected():
    pass # TODO - this should not be a unit test, rather an integration test?

def test_openai_no_access_to_model():
    pass # TODO - this should not be a unit test, rather an integration test?


# Prompt file

def test_prompt_file_missing():
    with pytest.raises(PromptError):
        copilot = OpenCopilot(
            prompt_file="this file definitely should not exist.mikrofilm"
        )

def test_prompt_file_invalid():
    with pytest.raises(PromptError):
        copilot = OpenCopilot(
            prompt_file="tests/assets/prompts/no_user_question.txt"
        )


# KB

def test_weaviate_not_running():
    pass # TODO - this should not be a unit test, rather an integration test?