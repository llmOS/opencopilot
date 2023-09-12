import os

from opencopilot.domain.errors import APIKeyError
from opencopilot.domain.errors import PromptError
from opencopilot.domain.errors import ModelError
from opencopilot.domain.chat.models.local import LocalLLM


def validate_prompt_and_prompt_file_config(prompt: str, prompt_file: str):
    if prompt and prompt_file:
        raise PromptError(
            "You can only pass either a prompt or a prompt_file argument, not both."
        )
    if not prompt and not prompt_file:
        raise PromptError("You need to pass either a prompt or a prompt_file argument.")

    if prompt_file and not os.path.isfile(prompt_file):
        raise PromptError(
            f"Prompt file '{prompt_file}' does not exist. Please make sure your prompt file path points to a file that exists."
        )


def validate_system_prompt(prompt: str):
    if not "{question}" in prompt:
        raise PromptError(
            f"Template variable '{{question}}' is missing in prompt. Please make sure your prompt file includes all required template variables."
        )
    if not "{history}" in prompt:
        raise PromptError(
            f"Template variable '{{history}}' is missing in prompt. Please make sure your prompt file includes all required template variables."
        )
    if not "{context}" in prompt:
        raise PromptError(
            f"Template variable '{{context}}' is missing in prompt. Please make sure your prompt file includes all required template variables."
        )


def validate_openai_api_key(key: str):
    if not key:
        raise APIKeyError(
            "OpenAI API key is empty or missing. Please add your OpenAI API key either as an environment variable, or an argument to the OpenCopilot() constructor."
        )
    if len(key) != 51 or not key.startswith("sk-"):
        raise APIKeyError(
            "OpenAI API key format is incorrect. Please check that you've entered a correct OpenAI API key."
        )


def validate_local_llm(llm: LocalLLM):
    try:
        llm.get_num_tokens("test")
    except:
        raise ModelError(
            f"Failed to use local LLM.\nMake sure it is running at {llm.llm_url}"
        )


def validate_settings(openai_api_key: str):
    validate_openai_api_key(openai_api_key)
