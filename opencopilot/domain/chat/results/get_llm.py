from typing import Dict, Optional

import openai
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseChatModel

from opencopilot import settings


def execute(user_id: str = None, streaming: bool = False) -> BaseChatModel:
    llm = settings.get().LLM
    if isinstance(llm, str):
        if settings.get().HELICONE_API_KEY:
            openai.api_base = settings.get().HELICONE_BASE_URL
        return ChatOpenAI(
            temperature=0.0,
            model_name=settings.get().LLM,
            streaming=streaming,
            model_kwargs={"headers": _get_headers(user_id)},
            openai_api_key=settings.get().OPENAI_API_KEY,
        )
    if hasattr(llm, "streaming"):
        llm.streaming = streaming
    return llm


def _get_headers(user_id: str = None) -> Optional[Dict]:
    if settings.get().HELICONE_API_KEY:
        headers = {
            "Helicone-Auth": "Bearer " + settings.get().HELICONE_API_KEY,
            "Helicone-User-Id": user_id or "",
        }
        if user_id and settings.get().HELICONE_RATE_LIMIT_POLICY:
            headers[
                "Helicone-RateLimit-Policy"
            ] = settings.get().HELICONE_RATE_LIMIT_POLICY
        return headers
    return None
