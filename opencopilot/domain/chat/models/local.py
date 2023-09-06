import requests
from typing import List
from urllib.parse import urljoin
from langchain.chat_models import ChatOpenAI
from opencopilot.logger import api_logger

logger = api_logger.get()


class LocalLLM(ChatOpenAI):
    openai_api_key: str = "LOCAL_LLM"
    llm_url: str = None

    def __init__(self, *args, **kwargs):
        kwargs.pop("openai_api_base", None)
        max_tokens = kwargs.pop("max_tokens", None) or 1024
        super().__init__(*args, **kwargs, openai_api_base=kwargs["llm_url"], max_tokens=max_tokens)

    def get_token_ids(self, text: str) -> List[int]:
        try:
            result = requests.post(
                urljoin(self.llm_url, "/v1/tokenize"), json={"prompt": text}
            )
            return result.json()["prompt_tokens"]
        except Exception as e:
            logger.error("Failed to get token count: %s", e)
