from opencopilot.settings import Settings


def test_get_base_url():
    settings = Settings(
        COPILOT_NAME="str",
        HOST="str",
        API_PORT=123,
        ENVIRONMENT="str",
        ALLOWED_ORIGINS="str",
        LLM="str",
        EMBEDDING_MODEL="str",
    )
    result = settings.get_base_url()
    assert result == "http://str:123"


def test_get_base_url_ends_with_slash():
    settings = Settings(
        COPILOT_NAME="str",
        HOST="str/",
        API_PORT=123,
        ENVIRONMENT="str",
        ALLOWED_ORIGINS="str",
        LLM="str",
        EMBEDDING_MODEL="str",
    )
    result = settings.get_base_url()
    assert result == "http://str:123"


def test_get_base_url_starts_with_http():
    settings = Settings(
        COPILOT_NAME="str",
        HOST="http://127.0.0.1/",
        API_PORT=123,
        ENVIRONMENT="str",
        ALLOWED_ORIGINS="str",
        LLM="str",
        EMBEDDING_MODEL="str",
    )
    result = settings.get_base_url()
    assert result == "http://127.0.0.1:123"
