import os
from opencopilot.domain.errors import PromptError, APIKeyError


def validate_system_prompt(file_path: str):
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            prompt = f.read()
            if not "{question}" in prompt:
                raise PromptError(
                    f"Template variable '{{question}}' is missing in prompt file '{file_path}'. Please make sure your prompt file includes all required template variables."
                )
            if not "{history}" in prompt:
                raise PromptError(
                    f"Template variable '{{history}}' is missing in prompt file '{file_path}'. Please make sure your prompt file includes all required template variables."
                )
            if not "{context}" in prompt:
                raise PromptError(
                    f"Template variable '{{context}}' is missing in prompt file '{file_path}'. Please make sure your prompt file includes all required template variables."
                )
    else:
        raise PromptError(
            f"Prompt file '{file_path}' does not exist. Please make sure your prompt file path points to a file that exists."
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
