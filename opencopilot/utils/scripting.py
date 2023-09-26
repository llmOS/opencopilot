import os
from typing import Optional

from opencopilot import settings
from opencopilot.settings import Settings


def set_default_settings(name: str = "script"):
    app_conf: Optional[settings.AppConf] = settings.AppConf.get()
    settings.set(
        Settings(
            COPILOT_NAME=app_conf.copilot_name if app_conf else name,
            HOST="127.0.0.1",
            API_PORT=app_conf.api_port if app_conf else 3000,
            ENVIRONMENT=name,
            ALLOWED_ORIGINS="*",
            WEAVIATE_URL="http://localhost:8080/",
            WEAVIATE_READ_TIMEOUT=120,
            LLM="gpt-4",
            EMBEDDING_MODEL="text-embedding-ada-002",
            OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"),
            MAX_DOCUMENT_SIZE_MB=1,
            AUTH_TYPE=None,
            API_KEY="",
            JWT_CLIENT_ID="",
            JWT_CLIENT_SECRET="",
            JWT_TOKEN_EXPIRATION_SECONDS=1,
            HELICONE_API_KEY="",
            HELICONE_RATE_LIMIT_POLICY="",
            TRACKING_ENABLED=os.environ.get("OPENCOPILOT_DO_NOT_TRACK", "").lower()
            != "True",
        )
    )
