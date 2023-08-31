import os
from pathlib import Path

from dotenv import load_dotenv

from opencopilot import OpenCopilot

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

copilot = OpenCopilot(
    prompt_file="my_prompt.txt",

    auth_type=os.getenv("AUTH_TYPE"),
    jwt_client_id=os.getenv("JWT_CLIENT_ID"),
    jwt_client_secret=os.getenv("JWT_CLIENT_SECRET"),
)
copilot()
