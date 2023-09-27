"""
Lightyear copilot

Prerequisite:

Key Components:

Environment Variables:

Usage:

"""
import json
from typing import Dict
from typing import List

import requests
from langchain.schema import Document

from examples.lightyear_copilot import call_copilot_use_case
from examples.lightyear_copilot import external_router_use_case
from examples.lightyear_copilot import get_user_info_use_case
from examples.lightyear_copilot.external_router_use_case import ExternalRoute
from opencopilot import OpenCopilot
from opencopilot.callbacks import ContextInput

IS_INCLUDE_COPILOT_NETWORK = False

COPILOT_NAME = "Lightyear Copilot"
copilot = OpenCopilot(
    prompt_file="prompt_template_no_context.txt",
    copilot_name=COPILOT_NAME,
    llm="gpt-4",
    api_port=3001,
    auth_type="jwt",
    jwt_client_id="string",
    jwt_client_secret="string",
    copilot_icon="https://lightyear.com/resources/favicon/favicon-32x32.png"
)


def _get_instruments() -> List[Dict]:
    res = requests.get("https://lightyear.com/api/v1/instrument")
    return res.json()


instruments: List[Dict] = _get_instruments()


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
    external_route = None
    if IS_INCLUDE_COPILOT_NETWORK:
        external_route = external_router_use_case.execute(context_input.message, copilots)
    if external_route and external_route.type != "self":
        return await call_copilot_use_case.execute(
            external_route.url,
            external_route.name,
            context_input
        )
    else:
        docs = await get_user_info_use_case.execute(context_input.user_id, instruments)
        return docs

copilot()
