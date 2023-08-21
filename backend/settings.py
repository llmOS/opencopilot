import json
import os
from pathlib import Path
from typing import Optional
from datetime import timedelta

from dotenv import load_dotenv
from omegaconf import OmegaConf

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

API_PORT = int(os.getenv("API_PORT", 3000))
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1/")
ENVIRONMENT = os.getenv("PLATFORM_ENVIRONMENT", "local")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")
APPLICATION_NAME = os.getenv("APPLICATION_NAME", "backend-service")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/logs-backend-service.log")

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "")
assert WEAVIATE_URL
WEAVIATE_READ_TIMEOUT = int(os.getenv("WEAVIATE_READ_TIMEOUT", 120))

MODEL = os.getenv("MODEL", "gpt-3.5-turbo-16k")
assert MODEL in ["gpt-3.5-turbo-16k", "gpt-4"], 'Model must be "gpt-3.5-turbo-16k" or "gpt-4".'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_URL = os.getenv("MODEL_URL", "")
assert OPENAI_API_KEY, "OPEN_AI_API_KEY must be set."

CONVERSATIONS_DIR: str = "conversations"
# Configure based on model?
PROMPT_HISTORY_INCLUDED_COUNT: int = 4
MAX_CONTEXT_DOCUMENTS_COUNT: int = 4
MAX_TOKEN_COUNT: int = 2048
MAX_DOCUMENT_SIZE_MB = int(os.getenv("MAX_DOCUMENT_SIZE_MB", 50))

COPILOT_NAME = os.getenv("COPILOT_NAME", "rpm")
COPILOT_DIRECTORY = f"../copilots/{COPILOT_NAME}"

UNITY_COPILOT_URL = os.getenv("UNITY_COPILOT_URL", "")
FUNCTIONS_MODEL = os.getenv("FUNCTIONS_MODEL", "gpt-4-0613")

PROMPTS_DIRECTORY = f"{COPILOT_DIRECTORY}/prompts/"


copilot_config = OmegaConf.load(f'{COPILOT_DIRECTORY}/config.yaml')


def _get_prompt_key(key: str) -> Optional[str]:
    try:
        with open(f"{COPILOT_DIRECTORY}/prompts/prompt_configuration.json", "r") as f:
            prompt_configuration = json.load(f)
        return prompt_configuration.get(key) or None
    except:
        pass
    return None


PROMPT_QUESTION_KEY = _get_prompt_key("question_key") or "Prompt"
PROMPT_ANSWER_KEY = _get_prompt_key("response_key") or "Response"


def get_max_token_count() -> int:
    if MODEL == "gpt-3.5-turbo-16k":
        return 16384
    if MODEL == "gpt-4":
        return 8192
    return 2048


DATA_DIR = f"{COPILOT_DIRECTORY}/data/"

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK", "")


def is_production():
    return ENVIRONMENT == "production"


COPILOTS_ROOT_PATH = "copilots"
API_KEY: str = os.getenv("API_KEY", "")

HELICONE_BASE_URL = "https://oai.hconeai.com/v1"
HELICONE_API_KEY: str = os.getenv("HELICONE_API_KEY", "")
HELICONE_RATE_LIMIT_POLICY: Optional[str] = os.getenv("HELICONE_RATE_LIMIT_POLICY", None)

AUTH_TYPE = os.getenv("AUTH_TYPE", "")
if AUTH_TYPE == "none" or AUTH_TYPE == "None" or AUTH_TYPE.strip() == "":
    AUTH_TYPE = None

JWT_CLIENT_ID: str = os.getenv("JWT_CLIENT_ID", "")
JWT_CLIENT_SECRET: str = os.getenv("JWT_CLIENT_SECRET", "")
JWT_TOKEN_EXPIRATION_SECONDS: int = int(os.getenv("JWT_TOKEN_EXPIRATION_SECONDS", timedelta(days=1).total_seconds()))
