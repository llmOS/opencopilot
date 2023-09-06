from dataclasses import dataclass
from typing import Literal
from typing import Optional


@dataclass(frozen=False)
class Settings:
    COPILOT_NAME: str

    HOST: str
    API_PORT: int
    API_BASE_URL: str
    ENVIRONMENT: str
    ALLOWED_ORIGINS: str

    WEAVIATE_URL: Optional[str]
    WEAVIATE_READ_TIMEOUT: int

    MODEL: Literal["gpt-3.5-turbo-16k", "gpt-4"]

    OPENAI_API_KEY: str

    MAX_DOCUMENT_SIZE_MB: int

    SLACK_WEBHOOK: str

    AUTH_TYPE: Optional[str]
    API_KEY: str

    JWT_CLIENT_ID: str
    JWT_CLIENT_SECRET: str
    JWT_TOKEN_EXPIRATION_SECONDS: int

    HELICONE_API_KEY: str
    HELICONE_RATE_LIMIT_POLICY: str

    TRACKING_ENABLED: bool = False

    CONVERSATIONS_DIR: str = "logs/conversations"
    # Configure based on model?
    PROMPT_HISTORY_INCLUDED_COUNT: int = 4
    MAX_CONTEXT_DOCUMENTS_COUNT: int = 4

    PROMPT: Optional[str] = None

    HELICONE_BASE_URL = "https://oai.hconeai.com/v1"

    def __post_init__(self):
        if self.AUTH_TYPE is not None and (
            self.AUTH_TYPE == "none"
            or self.AUTH_TYPE == "None"
            or self.AUTH_TYPE.strip() == ""
        ):
            self.AUTH_TYPE = None

        self.PROMPT_QUESTION_KEY = "User"
        self.PROMPT_ANSWER_KEY = "Copilot"

    def is_production(self):
        return self.ENVIRONMENT == "production"

    def get_max_token_count(self) -> int:
        if self.MODEL == "gpt-3.5-turbo-16k":
            return 16384
        if self.MODEL == "gpt-4":
            return 8192
        return 2048


_settings: Optional[Settings] = None


def get() -> Optional[Settings]:
    global _settings
    return _settings


def set(new_settings: Settings):
    global _settings
    _settings = new_settings
