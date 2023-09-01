import uuid
from typing import Dict

import requests

from opencopilot.scripts import chat
from opencopilot.scripts import get_jwt_token

conversation_id = uuid.uuid4()
base_url = f"http://0.0.0.0:3000"

message_id: str = ""


def _index():
    url = f"{base_url}/"
    result = requests.get(url)
    print(f"\nresult from GET {url}\n  {result}")
    assert result.status_code == 200
    assert result.json()


def _chat_conversation():
    result = chat.conversation(
        base_url=base_url,
        conversation_id=conversation_id
    )
    url = f"{base_url}/v0/conversations/{conversation_id}"
    print(f"\nresult from POST {url}\n  {result}")
    print("  json:", result.json(), "\n")
    assert result.json()["copilot_message"]


def _chat_conversation_stream():
    result = chat.conversation_stream(
        base_url=base_url,
        conversation_id=conversation_id
    )
    url = f"{base_url}/v0/conversations/{conversation_id}/stream"
    print(f"\nresult from POST {url}\n  {result}")
    assert result


def _chat_history(headers: Dict):
    url = f"{base_url}/v0/conversations/{conversation_id}"
    result = requests.get(url, headers=headers)
    print(f"\nresult from GET {url}\n  {result}")
    print("  json:", result.json(), "\n")
    assert result.json()["response"] == "OK"
    assert len(result.json()["messages"]) > 1
    global message_id
    message_id = result.json()["messages"][0]["response_message_id"]


def _conversations(headers: Dict):
    url = f"{base_url}/v0/conversations/"
    result = requests.get(url, headers=headers)
    print(f"\nresult from GET {url}\n  {result}")
    print("  json:", result.json(), "\n")
    assert result.json()["response"] == "OK"


def _conversation(headers: Dict):
    url = f"{base_url}/v0/conversations/{conversation_id}"
    result = requests.get(url, headers=headers)
    print(f"\nresult from GET {url}\n  {result}")
    print("  json:", result.json(), "\n")
    assert result.json()["response"] == "OK"


def _delete_conversations(headers: Dict):
    url = f"{base_url}/v0/conversations/{conversation_id}"
    result = requests.delete(url, headers=headers)
    print(f"\nresult from DELETE {url}\n  {result}")
    print("  json:", result.json(), "\n")
    assert result.json()["response"] == "OK"


def _debug(headers: Dict):
    url = f"{base_url}/v0/debug/{conversation_id}/{message_id}"
    result = requests.get(url, headers=headers)
    print(f"\nresult from GET {url}\n  {result}")
    print("  json:", result.json(), "\n")
    assert result.json()["response"] == "OK"
    assert result.json()["prompt_template"]
    assert result.json()["user_question"]
    assert result.json()["context"]
    assert result.json()["full_prompt"]
    assert result.json()["llm_response"]


def _get_headers():
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    jwt_token = get_jwt_token.execute(base_url)
    if jwt_token:
        headers["Authorization"] = "Bearer " + jwt_token
    return headers


def main():
    headers = _get_headers()
    _index()
    _chat_conversation()
    _chat_conversation_stream()
    _chat_history(headers)
    _conversations(headers)
    _conversation(headers)
    _debug(headers)
    _delete_conversations(headers)


if __name__ == '__main__':
    main()
