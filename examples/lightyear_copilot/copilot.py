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
from examples.lightyear_copilot import external_router_use_case
from examples.lightyear_copilot.external_router_use_case import ExternalRoute
from opencopilot import OpenCopilot
from opencopilot.callbacks import ContextInput

COPILOT_NAME = "Lightyear Copilot"
copilot = OpenCopilot(
    prompt_file="prompt_template.txt",
    copilot_name=COPILOT_NAME,
    llm="gpt-4",
    api_port=3001,
)

copilot.add_local_files_dir("data")


@copilot.context_builder
async def call_copilot(context_input: ContextInput) -> List[Document]:
    copilots = [
        ExternalRoute(
            type="self",
            url="",
            description="Useful for retrieving information related to user investments and portfolio",
            name=COPILOT_NAME,
        ),
        ExternalRoute(
            url="http://localhost:3000",
            description="Useful for retrieving information about the market and stocks in general",
            name="Analyst copilot"
        ),
    ]
    external_route = external_router_use_case.execute(context_input.message, copilots)
    if external_route and external_route.type != "self":
        return await call_copilot_use_case.execute(
            external_route.url,
            external_route.name,
            context_input
        )
    else:
        return []


copilot()
