import uuid
from typing import List
from urllib.parse import urljoin

import aiohttp
from langchain.schema import Document

from opencopilot import ContextInput


async def execute(base_url: str, copilot_name: str, context_input: ContextInput) -> List[Document]:
    docs: List[Document] = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                urljoin(base_url, f"/v0/conversations/{uuid.uuid4()}"),
                json={
                    "message": context_input.message,
                    #  TODO: add other context like history
                },
            ) as response:
                response.raise_for_status()
                response_json = await response.json()
                if copilot_message := response_json.get("copilot_message"):
                    docs.append(Document(
                        page_content=copilot_message,
                        metadata={
                            "source": copilot_name
                        }
                    ))
    except Exception as e:
        print(e)
    return docs
