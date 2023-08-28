import uuid

from opencopilot.scripts import chat

conversation_id = uuid.uuid4()
base_url = f"http://0.0.0.0:3000"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}


def _chat_conversation(message: str, expected: str):
    result = chat.conversation(
        base_url=base_url,
        conversation_id=conversation_id,
        message=message
    )
    url = f"{base_url}/v0/conversation/{conversation_id}"
    print(f"\nresult from {url}\n  {result}")
    print("  json:", result.json(), "\n")
    text = result.json()["generated_text"]
    assert expected in text


def _chat_conversation_stream(message: str, expected: str):
    result = chat.conversation_stream(
        base_url=base_url,
        conversation_id=uuid.uuid4(),
        message=message
    )
    url = f"{base_url}/v0/conversation_stream/{conversation_id}"
    print(f"\nresult from {url}\n  {result}")
    assert expected in result


def test():
    _chat_conversation_stream("Who is Estonian president?", "on Alar Karis")
    _chat_conversation("Who was last Estonian president?", "oli Kersti Kaljulaid")


if __name__ == '__main__':
    test()
