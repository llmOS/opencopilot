import json
import os
from dataclasses import dataclass
from typing import Literal
from typing import Optional
from omegaconf import OmegaConf
from opencopilot.utils.validators import validate_system_prompt


@dataclass(frozen=False)
class Settings:
    COPILOT_NAME: str

    HOST: str
    API_PORT: int
    API_BASE_URL: str
    ENVIRONMENT: str
    ALLOWED_ORIGINS: str
    APPLICATION_NAME: str
    LOG_FILE_PATH: str

    WEAVIATE_URL: str
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

    CONVERSATIONS_DIR: str = "logs/conversations"
    # Configure based on model?
    PROMPT_HISTORY_INCLUDED_COUNT: int = 4
    MAX_CONTEXT_DOCUMENTS_COUNT: int = 4
    MAX_TOKEN_COUNT: int = 2048

    PROMPT_FILE: Optional[str] = None

    HELICONE_BASE_URL = "https://oai.hconeai.com/v1"

    DATA_DIR: str = ""

    def __post_init__(self):
        os.environ["OPENAI_API_KEY"] = self.OPENAI_API_KEY

        if self.AUTH_TYPE is not None and (
            self.AUTH_TYPE == "none"
            or self.AUTH_TYPE == "None"
            or self.AUTH_TYPE.strip() == ""
        ):
            self.AUTH_TYPE = None

        self.COPILOT_DIRECTORY = f"copilots/{self.COPILOT_NAME}"

        self.PROMPT_QUESTION_KEY = self._get_prompt_key("question_key") or "User"
        self.PROMPT_ANSWER_KEY = self._get_prompt_key("response_key") or "Copilot"

    def is_production(self):
        return self.ENVIRONMENT == "production"

    def get_max_token_count(self) -> int:
        if self.MODEL == "gpt-3.5-turbo-16k":
            return 16384
        if self.MODEL == "gpt-4":
            return 8192
        return 2048

    def _get_prompt_key(self, key: str) -> Optional[str]:
        try:
            with open(
                f"{self.COPILOT_DIRECTORY}/prompts/prompt_configuration.json", "r"
            ) as f:
                prompt_configuration = json.load(f)
            return prompt_configuration.get(key) or None
        except:
            pass
        return None


def init_data_dir(data_dir: str) -> None:
    settings = get()
    if settings:
        settings.DATA_DIR = data_dir if os.path.exists(data_dir) else None


def init_custom_loaders(config_file: str) -> None:
    settings = get()
    if settings:
        try:
            settings.copilot_config = OmegaConf.load(config_file)
        except:
            pass


def init_prompt_file_location(file_path: str):
    settings = get()
    if settings:
        validate_system_prompt(file_path)
        settings.PROMPT_FILE = file_path


_settings: Optional[Settings] = None


def get() -> Optional[Settings]:
    global _settings
    return _settings


def set(new_settings: Settings):
    global _settings
    _settings = new_settings
