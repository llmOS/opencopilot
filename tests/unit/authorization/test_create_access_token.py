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
        COPILOT_NAME="str",
        HOST="str",
        API_PORT=123,
        ENVIRONMENT="str",
        ALLOWED_ORIGINS="str",
        LLM="str",
        EMBEDDING_MODEL="str",
        JWT_CLIENT_ID="valid_client_id",
        JWT_CLIENT_SECRET="valid_client_secret",
        JWT_TOKEN_EXPIRATION_SECONDS=3600
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
