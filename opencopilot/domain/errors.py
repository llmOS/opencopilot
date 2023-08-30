class CopilotConfigurationError(Exception):
    """Raised when the copilot configuration is invalid."""

    pass


class APIKeyError(CopilotConfigurationError):
    """Raised when an API key is not provided, malformed, or rejected by the API provider."""

    pass


class ModelError(CopilotConfigurationError):
    """Raised when the model passed in is invalid."""

    pass


class PromptError(CopilotConfigurationError):
    """Raised when the prompt file passed in is missing or invalid."""

    pass
