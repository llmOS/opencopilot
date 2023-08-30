import os

from opencopilot import OpenCopilot

copilot = OpenCopilot(
    prompt_file="prompts/prompt_template.txt",
    copilot_name="Parrot Copilot",
    host=os.getenv("HOST", "127.0.0.1"),
    api_port=int(os.getenv("PORT", 8080)),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    # weaviate_url=os.getenv("WEAVIATE_URL"),
)
copilot()
