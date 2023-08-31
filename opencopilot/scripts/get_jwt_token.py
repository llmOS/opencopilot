import os
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv

HEADERS = {"accept": "application/json", "Content-Type": "application/json"}


def execute(base_url: str) -> Optional[str]:
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)
    jwt_client_id = os.getenv("JWT_CLIENT_ID", "")
    jwt_client_secret = os.getenv("JWT_CLIENT_SECRET", "")
    url = f"{base_url}/v0/tokens"
    data = {
        "client_id": jwt_client_id,
        "client_secret": jwt_client_secret,
        "user_id": "test@local.host",
    }
    try:
        token_result = requests.post(url, headers=HEADERS, json=data)
        result_json = token_result.json()
        return result_json["token"]
    except:
        return None
