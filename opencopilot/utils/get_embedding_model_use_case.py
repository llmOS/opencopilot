import pickle
from typing import List
from typing import Dict
from pydantic import PrivateAttr

import xxhash
from langchain.embeddings.base import Embeddings
from langchain.embeddings import OpenAIEmbeddings
from openai import OpenAIError

from opencopilot import settings
from opencopilot.domain.errors import OpenAIRuntimeError
from opencopilot.logger import api_logger

logger = api_logger.get()


class CachedEmbeddings:
    embeddings: Embeddings = PrivateAttr()
    _cache: Dict = PrivateAttr()
    _embeddings_cache_filename: str = PrivateAttr()

    def __init__(self, embeddings: Embeddings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._embeddings = embeddings
        self._cache = {}
        self._embeddings_cache_filename = (
            settings.get().COPILOT_NAME + "_embeddings_cache.pkl"
        )
        self._load_local_cache()

    def embed_documents(self, texts: List[str], **kwargs) -> List[List[float]]:
        return self._embed_documents_cached(texts)

    def embed_query(self, text: str) -> List[float]:
        return self._embeddings.embed_query(text)

    def _embed_documents_cached(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        try:
            for text in texts:
                text_hash = self._hash(text)
                # pylint: disable-next=no-member
                if embedding := self._cache.get(text_hash):
                    embeddings.append(embedding)
                else:
                    embedding = self._embeddings.embed_documents([text])[0]
                    # pylint: disable-next=no-member
                    self._cache[text_hash] = embedding
                    embeddings.append(embedding)
        except OpenAIError as exc:
            raise OpenAIRuntimeError(exc.user_message)
        return embeddings

    def _hash(self, text) -> str:
        return xxhash.xxh64(text.encode("utf-8")).hexdigest()

    def _load_local_cache(self):
        try:
            # pylint: disable-next=no-member
            with open(self._embeddings_cache_filename, "rb") as f:
                data = pickle.load(f)
                self._cache = data
        except:
            pass

    def save_local_cache(self):
        try:
            with open(self._embeddings_cache_filename, "wb") as f:
                pickle.dump(self._cache, f)
        except Exception as e:
            logger.warning(
                f"Failed to save embeddings cache to {self._embeddings_cache_filename}"
            )


def execute():
    embeddings = settings.get().EMBEDDING_MODEL
    if isinstance(embeddings, str):
        openai_api_base = None
        headers = None
        if settings.get().HELICONE_API_KEY:
            openai_api_base = settings.get().HELICONE_BASE_URL
            headers = {
                "Helicone-Auth": "Bearer " + settings.get().HELICONE_API_KEY,
                "Helicone-Cache-Enabled": "true",
            }
        embeddings = OpenAIEmbeddings(
            disallowed_special=(),
            openai_api_base=openai_api_base,
            headers=headers,
            openai_api_key=settings.get().OPENAI_API_KEY,
        )
    return CachedEmbeddings(embeddings)
