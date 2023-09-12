import os
from opencopilot import settings
from opencopilot.settings import Settings


def set_default_settings(name: str = "script"):
    settings.set(
        Settings(
            COPILOT_NAME=name,
            HOST="127.0.0.1",
            API_PORT=3000,
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
