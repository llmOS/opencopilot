from abc import ABC


class CopilotConfigurationError(Exception, ABC):
    """Raised when the copilot configuration is invalid."""

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class PromptError(CopilotConfigurationError):
    """Raised when the prompt file passed in is missing or invalid."""


class APIKeyError(CopilotConfigurationError):
    """Raised when an API key is not provided, malformed, or rejected by the API provider."""

    pass


class ModelError(CopilotConfigurationError):
    """Raised when the model passed in is invalid."""

    pass


class LogsDirError(CopilotConfigurationError):
    """Raised when invalid logs dir was passed."""

    pass


class CopilotRuntimeError(Exception, ABC):
    """Raised when the copilot gets known run time exception."""

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class CopilotIsNotRunningError(CopilotRuntimeError):
    """Raised when cannot connect to Copilot"""


class OpenAIRuntimeError(CopilotRuntimeError):
    """Raised when cannot get a result from OpenAI"""


class WeaviateRuntimeError(CopilotRuntimeError):
    """Raised when cannot connect to Weaviate"""


class LocalLLMRuntimeError(CopilotRuntimeError):
    """Raised when error with connecting to LocalLLM"""
