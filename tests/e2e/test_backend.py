import uuid

import requests

from opencopilot.scripts import chat

conversation_id = uuid.uuid4()
base_url = f"http://0.0.0.0:3000"
HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json"
}


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


def _chat_history():
    url = f"{base_url}/v0/conversations/{conversation_id}"
    result = requests.get(url, headers=HEADERS)
    print(f"\nresult from GET {url}\n  {result}")
    print("  json:", result.json(), "\n")
    assert result.json()["response"] == "OK"
    assert len(result.json()["messages"]) > 1


def _conversations():
    url = f"{base_url}/v0/conversations/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "user-id": "test@tester.com"
    }
    result = requests.get(url, headers=headers)
    print(f"\nresult from GET {url}\n  {result}")
    print("  json:", result.json(), "\n")
    assert result.json()["response"] == "OK"


def _conversation():
    url = f"{base_url}/v0/conversations/{conversation_id}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "user-id": "test@tester.com"
    }
    result = requests.get(url, headers=headers)
    print(f"\nresult from GET {url}\n  {result}")
    print("  json:", result.json(), "\n")
    assert result.json()["response"] == "OK"


def _delete_conversations():
    url = f"{base_url}/v0/conversations/{conversation_id}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "user-id": "test@tester.com"
    }
    result = requests.delete(url, headers=headers)
    print(f"\nresult from DELETE {url}\n  {result}")
    print("  json:", result.json(), "\n")
    assert result.json()["response"] == "OK"


def main():
    _index()
    _chat_conversation()
    _chat_conversation_stream()
    _chat_history()
    _conversations()
    _conversation()
    _delete_conversations()


if __name__ == '__main__':
    main()
