from dataclasses import dataclass
from typing import Optional
from typing import Union

from langchain.chat_models.base import BaseChatModel
from langchain.embeddings.base import Embeddings

from opencopilot.domain.chat.models.local import LocalLLM


@dataclass(frozen=False)
class Settings:
    COPILOT_NAME: str

    HOST: str
    API_PORT: int
    ENVIRONMENT: str
    ALLOWED_ORIGINS: str

    LLM: Union[str, BaseChatModel]
    EMBEDDING_MODEL: Union[str, Embeddings]

    OPENAI_API_KEY: Optional[str] = None

    AUTH_TYPE: Optional[str] = None
    API_KEY: Optional[str] = None

    JWT_CLIENT_ID: Optional[str] = None
    JWT_CLIENT_SECRET: Optional[str] = None
    JWT_TOKEN_EXPIRATION_SECONDS: Optional[int] = 0

    HELICONE_API_KEY: Optional[str] = None
    HELICONE_RATE_LIMIT_POLICY: Optional[str] = None

    WEAVIATE_URL: Optional[str] = None
    WEAVIATE_READ_TIMEOUT: Optional[int] = 120

    MAX_DOCUMENT_SIZE_MB: Optional[int] = 50

    TRACKING_ENABLED: bool = False

    LOGS_DIR: str = "logs"
    # Configure based on model?
    PROMPT_HISTORY_INCLUDED_COUNT: int = 4
    MAX_CONTEXT_DOCUMENTS_COUNT: int = 4

    PROMPT: Optional[str] = None
    QUESTION_TEMPLATE: Optional[str] = None
    RESPONSE_TEMPLATE: Optional[str] = None

    HELICONE_BASE_URL = "https://oai.hconeai.com/v1"

    def __post_init__(self):
        if self.AUTH_TYPE is not None and (
            self.AUTH_TYPE == "none"
            or self.AUTH_TYPE == "None"
            or self.AUTH_TYPE.strip() == ""
        ):
            self.AUTH_TYPE = None

    def is_production(self):
        return self.ENVIRONMENT == "production"

    def get_max_token_count(self) -> int:
        if self.LLM == "gpt-3.5-turbo-16k":
            return 16384
        elif self.LLM == "gpt-4":
            return 8192
        elif isinstance(self.LLM, LocalLLM):
            return self.LLM.context_size
        return 2048

    def get_base_url(self) -> str:
        base_url = self.HOST
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        base_url += ":" + str(self.API_PORT)
        if not base_url.startswith("http://"):
            base_url = "http://" + base_url
        return base_url


_settings: Optional[Settings] = None


def get() -> Optional[Settings]:
    global _settings
    return _settings


def set(new_settings: Settings):
    global _settings
    _settings = new_settings
