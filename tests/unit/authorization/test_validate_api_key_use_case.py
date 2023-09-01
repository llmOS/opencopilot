import pytest
from unittest.mock import patch

from opencopilot import settings
from opencopilot.settings import Settings
from opencopilot.service import error_responses
import opencopilot.authorization.validate_api_key_use_case as use_case


@patch("opencopilot.authorization.validate_api_key_use_case.settings")
@pytest.mark.asyncio
async def test_execute_no_api_key(mock_settings):
    with pytest.raises(error_responses.AuthorizationMissingAPIError):
        await use_case.execute(api_key_header=None)


@patch("opencopilot.authorization.validate_api_key_use_case.settings")
@pytest.mark.asyncio
async def test_execute_invalid_api_key(mock_settings):
    mock_settings.API_KEY = "Valid key"
    with pytest.raises(error_responses.AuthorizationMissingAPIError):
        await use_case.execute(api_key_header="Invalid key")


@patch("opencopilot.authorization.validate_api_key_use_case.settings")
@patch("opencopilot.authorization.validate_api_key_use_case._validate_jwt")
@pytest.mark.asyncio
async def test_execute_bearer_api_key(mock_validate_jwt, mock_settings):
    mock_validate_jwt.return_value = "sub_value"
    result = await use_case.execute(api_key_header="Bearer valid_token")
    mock_validate_jwt.assert_called_once_with("valid_token")
    assert result == "sub_value"


@patch("opencopilot.authorization.validate_api_key_use_case.settings.get")
@patch("opencopilot.authorization.validate_api_key_use_case.jwt")
@pytest.mark.asyncio
async def test_validate_jwt_success(mock_jwt, mock_settings):
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

        JWT_CLIENT_ID="",
        JWT_CLIENT_SECRET="secret",
        JWT_TOKEN_EXPIRATION_SECONDS=3600,

        HELICONE_API_KEY="",
        HELICONE_RATE_LIMIT_POLICY="",
    )
    mock_settings.JWT_CLIENT_SECRET = "secret"
    mock_jwt.decode.return_value = {"sub": "sub_value"}
    result = await use_case._validate_jwt("valid_payload")
    mock_jwt.decode.assert_called_once_with("valid_payload", "secret", algorithms=["HS256"])
    assert result == "sub_value"


@patch("opencopilot.authorization.validate_api_key_use_case.settings")
@patch("opencopilot.authorization.validate_api_key_use_case.jwt")
@pytest.mark.asyncio
async def test_validate_jwt_failure(mock_jwt, mock_settings):
    mock_settings.JWT_CLIENT_SECRET = "secret"
    mock_jwt.decode.side_effect = Exception("Error")
    with pytest.raises(error_responses.AuthorizationMissingAPIError):
        await use_case._validate_jwt("invalid_payload")
