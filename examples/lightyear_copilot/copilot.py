"""
Lightyear copilot

Prerequisite:

Key Components:

Environment Variables:

Usage:

"""
from typing import List

from langchain.schema import Document

from examples.lightyear_copilot import call_copilot_use_case
from opencopilot import OpenCopilot
from opencopilot.callbacks import ContextInput

copilot = OpenCopilot(
    prompt_file="prompt_template.txt",
    copilot_name="Lightyear Copilot",
    api_port=3001,
)

copilot.add_local_files_dir("data")


@copilot.context_builder
async def call_copilot(context_input: ContextInput) -> List[Document]:
    # Check if its required to get the opinion of another copilot?
    return await call_copilot_use_case.execute(
        "http://localhost:3000",
        "Analyst copilot",
        context_input
    )


copilot()
