import uuid
from typing import List

from opencopilot.domain.cli import cli_chat_use_case

conversation_id = uuid.uuid4()
base_url = f"http://0.0.0.0:3000"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}


def _chat_conversation(message: str, expected: List[str]):
    result = cli_chat_use_case.conversation(
        base_url=base_url,
        conversation_id=conversation_id,
        message=message
    )
    url = f"{base_url}/v0/conversation/{conversation_id}"
    print(f"\nresult from {url}\n  {result}")
    print("  json:", result.json(), "\n")
    text = result.json()["copilot_message"]
    is_success = False
    for e in expected:
        if e in text:
            is_success = True
    assert is_success


def _chat_conversation_stream(message: str, expected: List[str]):
    result = cli_chat_use_case.conversation_stream(
        base_url=base_url,
        conversation_id=uuid.uuid4(),
        message=message
    )
    url = f"{base_url}/v0/conversation_stream/{conversation_id}"
    print(f"\nresult from {url}\n  {result}")
    is_success = False
    for e in expected:
        if e in result:
            is_success = True
    assert is_success


def test():
    _chat_conversation_stream(
        "Who is Estonian president?",
        ["on Alar Karis", "Alar Karis on"])
    _chat_conversation(
        "Who was last Estonian president?",
        ["oli Kersti Kaljulaid", "Kersti Kaljulaid oli"])
    _chat_conversation(
        "Who is the prime minister of Estonia?",
        ["Kaja Kallas"]
    )


if __name__ == '__main__':
    test()
