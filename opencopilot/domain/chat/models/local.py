import json
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from urllib.parse import urljoin

import aiohttp
import requests
from langchain.callbacks.manager import AsyncCallbackManagerForLLMRun
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.chat_models.base import BaseChatModel
from langchain.schema import AIMessage
from langchain.schema import BaseMessage
from langchain.schema import ChatGeneration
from langchain.schema import ChatResult
from pydantic import Extra

from opencopilot.domain import error_messages
from opencopilot.domain.errors import LocalLLMRuntimeError
from opencopilot.logger import api_logger

logger = api_logger.get()


class LocalLLM(BaseChatModel):
    context_size: int = 4096
    temperature: float = 0.7
    llm_url: str

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.ignore
        allow_population_by_field_name = True

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        final = ""
        for text in self._get_stream(
            {"query": messages[0], "temperature": self.temperature, "stop": stop}
        ):
            final += self._process_text(text)
        return ChatResult(
            generations=[
                ChatGeneration(
                    message=AIMessage(content=final),
                )
            ]
        )

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        final = ""
        try:
            async for text in self._get_async_stream(
                {
                    "query": messages[0].content,
                    "temperature": self.temperature,
                    "max_tokens": 0,
                }
            ):
                token = self._process_text(text)
                final += token
                if run_manager:
                    await run_manager.on_llm_new_token(token)
            return ChatResult(
                generations=[
                    ChatGeneration(
                        message=AIMessage(content=final),
                    )
                ]
            )
        except Exception as exc:
            raise LocalLLMRuntimeError(
                error_messages.LOCAL_LLM_CONNECTION_ERROR
            ) from exc

    def get_token_ids(self, text: str) -> List[int]:
        try:
            result = requests.post(
                urljoin(self.llm_url, "/tokenize"), json={"text": text}
            )
            return result.json()["tokens"]
        except Exception as exc:
            raise LocalLLMRuntimeError(
                error_messages.LOCAL_LLM_CONNECTION_ERROR
            ) from exc

    @property
    def _llm_type(self) -> str:
        return "local-llm"

    def _get_stream(self, payload: Dict):
        s = requests.Session()
        with s.post(
            urljoin(self.llm_url, "/generate_stream"), json=payload, stream=True
        ) as resp:
            for line in resp.iter_lines():
                if line:
                    yield line

    async def _get_async_stream(self, payload: Dict):
        timeout = aiohttp.ClientTimeout(sock_read=1200)
        async with aiohttp.ClientSession(timeout=timeout) as s:
            async with s.post(
                urljoin(self.llm_url, "/generate_stream"), json=payload
            ) as resp:
                async for line in resp.content.iter_any():
                    if line:
                        yield line

    def _process_text(self, line_raw):
        line = line_raw.decode("utf-8")
        try:
            line = line.replace('data:{"token"', '{"token"')
            line = json.loads(line)
            return line["token"]["text"]
        except:
            return ""
