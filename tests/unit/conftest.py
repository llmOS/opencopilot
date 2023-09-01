from unittest.mock import MagicMock

from opencopilot import settings
from opencopilot.logger import api_logger
from opencopilot.settings import Settings


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    settings.set(Settings(
        COPILOT_NAME="unit_tests",
        HOST="127.0.0.1",
        API_PORT=3000,
        API_BASE_URL="http://localhost:3000/",
        ENVIRONMENT="test",
        ALLOWED_ORIGINS="*",
        APPLICATION_NAME="unit_tests_app",
        LOG_FILE_PATH="mock",

        WEAVIATE_URL="mock_url",
        WEAVIATE_READ_TIMEOUT=120,

        MODEL="gpt-4",

        OPENAI_API_KEY="None",

        MAX_DOCUMENT_SIZE_MB=1,

        SLACK_WEBHOOK="",

        AUTH_TYPE=None,
        API_KEY="",

        JWT_CLIENT_ID="",
        JWT_CLIENT_SECRET="",
        JWT_TOKEN_EXPIRATION_SECONDS=1,

        HELICONE_API_KEY="",
        HELICONE_RATE_LIMIT_POLICY="",
    ))

    api_logger.get = MagicMock()
