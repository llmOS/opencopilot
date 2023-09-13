import json
import os
from uuid import UUID

from opencopilot.repository.conversation_history_repository import \
    ConversationHistoryRepositoryLocal

CONVERSATIONS_DIR = "tests/assets/conversations"
CONVERSATION_ID = UUID("79f88a74-7a67-4336-b601-4cfbcaed55ef")
CONVERSATION_ID_INVALID = UUID("79f88a74-7a67-4336-b601-4cfbcaed55e1")


def setup_function():
    create_mock_conversation()


def teardown_function():
    create_mock_conversation()


def create_mock_conversation():
    data = [
        {"prompt": "Prompt", "response": "Response"},
        {"prompt": "Prompt2", "response": "Response2"}
    ]
    file_path = os.path.join(CONVERSATIONS_DIR, str(CONVERSATION_ID)) + ".json"
    os.makedirs(CONVERSATIONS_DIR, exist_ok=True)
    with open(file_path, "w") as file:
        file.write(json.dumps(data, indent=4))


def test_get_prompt_history_default():
    repository = ConversationHistoryRepositoryLocal(
        CONVERSATIONS_DIR,
        question_template="MockQues: {question}",
        response_template="MockRes: {response}")
    result = repository.get_prompt_history(CONVERSATION_ID, 4)
    print("result:", result)
    expected = "MockQues: Prompt\nMockRes: Response\n" \
               "MockQues: Prompt2\nMockRes: Response2\n"
    assert result == expected


def test_get_prompt_history_count_1():
    repository = ConversationHistoryRepositoryLocal(
        CONVERSATIONS_DIR,
        question_template="MockQues: {question}",
        response_template="MockRes: {response}")
    result = repository.get_prompt_history(CONVERSATION_ID, 1)
    expected = "MockQues: Prompt2\nMockRes: Response2\n"
    assert result == expected


def test_get_prompt_history_not_found():
    repository = ConversationHistoryRepositoryLocal(
        CONVERSATIONS_DIR,
        question_template="MockQues: {question}",
        response_template="MockRes: {response}")
    result = repository.get_prompt_history(CONVERSATION_ID_INVALID, 1)
    assert result == ""


def test_get_history():
    repository = ConversationHistoryRepositoryLocal(
        CONVERSATIONS_DIR,
        question_template="MockQues: {question}",
        response_template="MockRes: {response}")
    result = repository.get_history(CONVERSATION_ID)
    expected = [
        {"prompt": "Prompt", "response": "Response"},
        {"prompt": "Prompt2", "response": "Response2"}
    ]
    assert result == expected


def test_get_history_not_found():
    repository = ConversationHistoryRepositoryLocal(
        CONVERSATIONS_DIR,
        question_template="MockQues: {question}",
        response_template="MockRes: {response}")
    result = repository.get_history(CONVERSATION_ID_INVALID)
    expected = []
    assert result == expected


def test_save_history():
    repository = ConversationHistoryRepositoryLocal(
        CONVERSATIONS_DIR,
        question_template="MockQues: {question}",
        response_template="MockRes: {response}")
    repository.save_history(
        message="Prompt3",
        result="Response3",
        conversation_id=CONVERSATION_ID,
        prompt_timestamp=123.12,
        response_timestamp=124.12,
        response_message_id="mock_id"
    )
    result = repository.get_history(CONVERSATION_ID)
    expected = [
        {"prompt": "Prompt", "response": "Response"},
        {"prompt": "Prompt2", "response": "Response2"},
        {"prompt": "Prompt3", "response": "Response3", "prompt_timestamp": 123.12,
         "response_timestamp": 124.12, "response_message_id": "mock_id"}
    ]
    assert result == expected


def test_remove_conversation():
    repository = ConversationHistoryRepositoryLocal(
        CONVERSATIONS_DIR,
        question_template="MockQues: {question}",
        response_template="MockRes: {response}")
    repository.remove_conversation(CONVERSATION_ID)
    result = repository.get_history(CONVERSATION_ID)
    print(result)
    assert result == []
