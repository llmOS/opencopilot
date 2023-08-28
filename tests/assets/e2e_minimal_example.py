import os

from opencopilot import OpenCopilot

copilot = OpenCopilot(
    prompt_file="my_prompt.txt",
    helicone_api_key=os.getenv("HELICONE_API_KEY")
)
copilot()
