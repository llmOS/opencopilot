import json
import os
import uuid
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv

headers = {"accept": "application/json", "Content-Type": "application/json"}
DEFAULT_MESSAGE = "Hi"


def _get_stream(url: str, message: str = DEFAULT_MESSAGE, jwt_token: str = None):
    data = {"message": message}
    if jwt_token:
        headers["Authorization"] = "Bearer " + jwt_token
    s = requests.Session()
    with s.post(url, headers=headers, json=data, stream=True) as resp:
        for line in resp.iter_lines():
            if line:
                yield line


def _process_text(line):
    line = line.decode("utf-8")
    try:
        line = json.loads(line)
        if error := line.get("error"):
            print("ERROR:", error)
            raise Exception("Error in stream")
        return line["text"]
    except:
        return ""


def conversation(
    base_url: str,
    conversation_id: uuid.UUID,
    message: str = DEFAULT_MESSAGE,
):
    jwt_token = _get_jwt_token(base_url)
    if jwt_token:
        headers["Authorization"] = "Bearer " + jwt_token
    url = f"{base_url}/v0/conversations/{conversation_id}"
    data = {"message": message}
    return requests.post(url, json=data, headers=headers)


def conversation_stream(
    base_url: str,
    conversation_id: uuid.UUID,
    message: str = DEFAULT_MESSAGE,
    stream: bool = False,
):
    jwt_token = _get_jwt_token(base_url)
    url = f"{base_url}/v0/conversations/{conversation_id}/stream"
    output = ""
    for text in _get_stream(url, message=message, jwt_token=jwt_token):
        text = _process_text(text)
        output += text
        if stream:
            print(text, end="", flush=True)
    return output


def _get_jwt_token(base_url: str) -> Optional[str]:
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)
    jwt_client_id = os.getenv("JWT_CLIENT_ID", "")
    jwt_client_secret = os.getenv("JWT_CLIENT_SECRET", "")
    url = f"{base_url}/v0/token"
    data = {
        "client_id": jwt_client_id,
        "client_secret": jwt_client_secret,
        "user_id": "test@local.host",
    }
    try:
        token_result = requests.post(url, headers=headers, json=data)
        result_json = token_result.json()
        return result_json["token"]
    except:
        return None


if __name__ == "__main__":
    _result = conversation_stream(
        # TODO: fix base_url
        base_url=f"http://0.0.0.0:3000",
        conversation_id=uuid.uuid4(),
    )
    print("result:", _result)
