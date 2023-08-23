import time
from unittest.mock import patch

import jwt
import pytest

import opencopilot.authorization.create_access_token as use_case
from opencopilot import settings
from opencopilot.settings import Settings
from opencopilot.service import error_responses


@patch("opencopilot.authorization.create_access_token.settings")
def test_execute_invalid_credentials(mock_settings):
    mock_settings.JWT_CLIENT_ID = "valid_client_id"
    mock_settings.JWT_CLIENT_SECRET = "valid_client_secret"
    with pytest.raises(error_responses.InvalidCredentialsAPIError):
        use_case.execute(client_id="invalid_client_id", client_secret="invalid_client_secret",
                         user_id="user_id")


@patch("opencopilot.authorization.create_access_token.settings.get")
@patch("opencopilot.authorization.create_access_token.time")
def test_execute_valid_credentials(mock_time, mock_settings):
    settings.get.return_value = Settings(
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

        JWT_CLIENT_ID="valid_client_id",
        JWT_CLIENT_SECRET="valid_client_secret",
        JWT_TOKEN_EXPIRATION_SECONDS=3600,

        HELICONE_API_KEY="",
        HELICONE_RATE_LIMIT_POLICY="",
    )
    # generate 1 second old token
    current_timestamp = time.time() - 1
    mock_time.time.return_value = current_timestamp
    result = use_case.execute(
        client_id="valid_client_id",
        client_secret="valid_client_secret",
        user_id="user_id")

    # Decode the resulting token to verify it contains the expected payload
    decoded = jwt.decode(result, "valid_client_secret", algorithms=["HS256"])

    assert decoded["sub"] == "user_id"
    assert decoded["iat"] == current_timestamp - 100
    assert decoded["exp"] == current_timestamp + 3600
