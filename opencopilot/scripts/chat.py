import json
import uuid

import requests

from opencopilot.scripts import get_jwt_token

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
    jwt_token = get_jwt_token.execute(base_url)
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
    jwt_token = get_jwt_token.execute(base_url)
    url = f"{base_url}/v0/conversations/{conversation_id}/stream"
    output = ""
    for text in _get_stream(url, message=message, jwt_token=jwt_token):
        text = _process_text(text)
        output += text
        if stream:
            print(text, end="", flush=True)
    return output


if __name__ == "__main__":
    _result = conversation_stream(
        # TODO: fix base_url
        base_url=f"http://0.0.0.0:3000",
        conversation_id=uuid.uuid4(),
    )
    print("result:", _result)
