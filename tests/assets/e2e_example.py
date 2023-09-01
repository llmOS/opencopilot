import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.schema import Document

from opencopilot import OpenCopilot

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

copilot = OpenCopilot(
    prompt_file="tests/assets/e2e_example_prompt.txt",
    helicone_api_key=os.getenv("HELICONE_API_KEY"),
    auth_type=os.getenv("AUTH_TYPE"),
    jwt_client_id=os.getenv("JWT_CLIENT_ID"),
    jwt_client_secret=os.getenv("JWT_CLIENT_SECRET"),
)
copilot.add_local_files_dir("tests/assets/e2e_example_data")


@copilot.data_loader
def e2e_data_loader():
    return [
        Document(
            page_content="Estonian last president was Kersti Kaljulaid",
            metadata={"source": "internet"}
        )
    ]


copilot()
