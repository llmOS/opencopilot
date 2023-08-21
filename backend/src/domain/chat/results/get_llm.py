from typing import Dict, Optional

import openai
from langchain.chat_models import ChatOpenAI

import settings
from src.utils.callbacks.callback_handler import CustomAsyncIteratorCallbackHandler


def execute(
        email: str = None,
        callback: CustomAsyncIteratorCallbackHandler = None,
) -> ChatOpenAI:
    if settings.HELICONE_API_KEY:
        openai.api_base = settings.HELICONE_BASE_URL
    llm = ChatOpenAI(
        temperature=0.0,
        model_name=settings.MODEL,
        streaming=callback is not None,
        callbacks=[callback] if callback is not None else None,
        headers=_get_headers(email)
    )
    return llm


def _get_headers(email: str = None) -> Optional[Dict]:
    if settings.HELICONE_API_KEY:
        headers = {
            "Helicone-Auth": "Bearer " + settings.HELICONE_API_KEY,
            "Helicone-User-Id": email or "",
        }
        if email and settings.HELICONE_RATE_LIMIT_POLICY:
            headers["Helicone-RateLimit-Policy"] = settings.HELICONE_RATE_LIMIT_POLICY
        return headers
    return None
