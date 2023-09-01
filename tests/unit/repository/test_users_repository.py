import json
import os
from uuid import UUID

from opencopilot.repository.users_repository import UsersRepositoryLocal

USERS_DIR = "tests/assets/users"

VALID_USER_ID = "test@tester.com"
INVALID_USER_ID = "test2@tester.com"


def setup_function():
    create_mock_user()


def teardown_function():
    create_mock_user()


def create_mock_user():
    file_path = os.path.join(USERS_DIR, "a449a63e0d25c897") + ".json"
    data = {
        "conversations": [
            "69f88a74-7a67-4336-b601-4cfbcaed55ef",
            "79f88a74-7a67-4336-b601-4cfbcaed55ef",
        ]
    }
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4))


def test_get_with_valid_user_id():
    repository = UsersRepositoryLocal(users_dir=USERS_DIR)
    result = repository.get_conversations(VALID_USER_ID)
    assert result == [
        "69f88a74-7a67-4336-b601-4cfbcaed55ef",
        "79f88a74-7a67-4336-b601-4cfbcaed55ef",
    ]


def test_get_with_invalid_user_id():
    repository = UsersRepositoryLocal(users_dir=USERS_DIR)
    result = repository.get_conversations("invalid@random")
    assert result == []


def test_get_no_user_id():
    repository = UsersRepositoryLocal(users_dir=USERS_DIR)
    result = repository.get_conversations()
    assert result == []


def test_add():
    repository = UsersRepositoryLocal(users_dir=USERS_DIR)
    repository.add_conversation(
        conversation_id=UUID("89f88a74-7a67-4336-b601-4cfbcaed55ef"),
        user_id=VALID_USER_ID)
    result = repository.get_conversations(VALID_USER_ID)
    assert result == [
        "69f88a74-7a67-4336-b601-4cfbcaed55ef",
        "79f88a74-7a67-4336-b601-4cfbcaed55ef",
        "89f88a74-7a67-4336-b601-4cfbcaed55ef",
    ]


def test_add_multiple_times():
    repository = UsersRepositoryLocal(users_dir=USERS_DIR)
    repository.add_conversation(
        conversation_id=UUID("89f88a74-7a67-4336-b601-4cfbcaed55ef"),
        user_id=VALID_USER_ID)
    repository.add_conversation(
        conversation_id=UUID("89f88a74-7a67-4336-b601-4cfbcaed55ef"),
        user_id=VALID_USER_ID)
    result = repository.get_conversations(VALID_USER_ID)
    assert result == [
        "69f88a74-7a67-4336-b601-4cfbcaed55ef",
        "79f88a74-7a67-4336-b601-4cfbcaed55ef",
        "89f88a74-7a67-4336-b601-4cfbcaed55ef",
    ]


def test_remove_existing():
    repository = UsersRepositoryLocal(users_dir=USERS_DIR)
    repository.remove_conversation(
        conversation_id=UUID("79f88a74-7a67-4336-b601-4cfbcaed55ef"),
        user_id=VALID_USER_ID
    )
    result = repository.get_conversations(VALID_USER_ID)
    assert result == [
        "69f88a74-7a67-4336-b601-4cfbcaed55ef",
    ]


def test_remove_non_existing():
    repository = UsersRepositoryLocal(users_dir=USERS_DIR)
    repository.remove_conversation(
        conversation_id=UUID("99f88a74-7a67-4336-b601-4cfbcaed55ef"),
        user_id=VALID_USER_ID
    )
    result = repository.get_conversations(VALID_USER_ID)
    assert result == [
        "69f88a74-7a67-4336-b601-4cfbcaed55ef",
        "79f88a74-7a67-4336-b601-4cfbcaed55ef",
    ]


def test_remove_from_empty_history():
    repository = UsersRepositoryLocal(users_dir=USERS_DIR)
    repository.remove_conversation(
        conversation_id=UUID("69f88a74-7a67-4336-b601-4cfbcaed55ef"),
        user_id=INVALID_USER_ID
    )
    result = repository.get_conversations(INVALID_USER_ID)
    print("result:", result)
    assert result == []
