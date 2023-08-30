import os
from typing import Optional
from uuid import UUID

from langchain.schema import Document

from opencopilot.repository.conversation_logs_repository import \
    ConversationLogsRepositoryLocal

CONVERSATION_LOGS_DIR = "tests/assets/conversation_logs"

CHAT_ID = UUID("79f88a74-7a67-4336-b601-4cfbcaed55ea")
CHAT_ID_INVALID = UUID("79f88a74-7a67-4336-b601-4cfbcaed55eb")

FILE_PATH = os.path.join(CONVERSATION_LOGS_DIR, str(CHAT_ID) + ".jsonl")


def setup_function():
    delete_file()


def teardown_function():
    delete_file()


def delete_file():
    try:
        os.remove(FILE_PATH)
    except:
        pass


def test_log_prompt_text():
    repository = ConversationLogsRepositoryLocal(CONVERSATION_LOGS_DIR)
    repository.log_prompt_text(CHAT_ID, "mock msg", "mock prompt text",
                               "mock-response-msg-id")
    result = _read_file()
    expected = '{"response_message_id": "mock-response-msg-id", ' \
               '"message": "mock msg", "prompt_text": "mock prompt text", ' \
               '"token_count": null}\n'
    assert result == expected


def test_log_prompt_text_with_tokens():
    repository = ConversationLogsRepositoryLocal(CONVERSATION_LOGS_DIR)
    repository.log_prompt_text(
        CHAT_ID,
        "mock msg",
        "mock prompt text",
        "mock-response-msg-id",
        token_count=1337,
    )
    result = _read_file()
    expected = '{"response_message_id": "mock-response-msg-id", ' \
               '"message": "mock msg", "prompt_text": "mock prompt text", ' \
               '"token_count": 1337}\n'
    assert result == expected


def test_log_context():
    repository = ConversationLogsRepositoryLocal(CONVERSATION_LOGS_DIR)
    repository.log_context(CHAT_ID, "mock msg", [Document(page_content="mock content")],
                           "mock-response-msg-id")
    result = _read_file()
    expected = '{"response_message_id": "mock-response-msg-id", "message": "mock msg", ' \
               '"context": "[{\\"page_content\\": \\"mock content\\", \\"metadata\\": {}}]", "token_count": null}\n'
    assert result == expected


def test_log_context_with_tokens():
    repository = ConversationLogsRepositoryLocal(CONVERSATION_LOGS_DIR)
    repository.log_context(
        CHAT_ID,
        "mock msg",
        [Document(page_content="mock content", metadata={"source": "secret"})],
        "mock-response-msg-id",
        token_count=1337,
    )
    result = _read_file()
    expected = '{"response_message_id": "mock-response-msg-id", "message": "mock msg", ' \
               '"context": "[{\\"page_content\\": \\"mock content\\", \\"metadata\\": {\\"source\\": \\"secret\\"}}]", "token_count": 1337}\n'
    assert result == expected


def test_remove_conversation():
    repository = ConversationLogsRepositoryLocal(CONVERSATION_LOGS_DIR)
    repository.log_context(
        CHAT_ID,
        "mock msg",
        [Document(page_content="mock content")],
        "mock-response-msg-id")
    repository.remove_conversation(CHAT_ID)
    result = _read_file()
    assert result is None


def _read_file() -> Optional[str]:
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            return file.read()
    return None
