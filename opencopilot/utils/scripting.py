import os
from opencopilot import settings
from opencopilot.settings import Settings


def set_default_settings(name: str = "script"):
    settings.set(
        Settings(
            COPILOT_NAME=name,
            HOST="127.0.0.1",
            API_PORT=3000,
            API_BASE_URL="http://localhost:3000/",
            ENVIRONMENT=name,
            ALLOWED_ORIGINS="*",
            APPLICATION_NAME=name,
            LOG_FILE_PATH=f"./logs/{name}.log",
            WEAVIATE_URL="http://localhost:8080/",
            WEAVIATE_READ_TIMEOUT=120,
            MODEL="gpt-4",
            OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"),
            MAX_DOCUMENT_SIZE_MB=1,
            SLACK_WEBHOOK="",
            AUTH_TYPE=None,
            API_KEY="",
            JWT_CLIENT_ID="",
            JWT_CLIENT_SECRET="",
            JWT_TOKEN_EXPIRATION_SECONDS=1,
            HELICONE_API_KEY="",
            HELICONE_RATE_LIMIT_POLICY="",
        )
    )
