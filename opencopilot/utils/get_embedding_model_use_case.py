import pickle
from typing import List

import xxhash
from langchain.embeddings import OpenAIEmbeddings

from opencopilot import settings
from opencopilot.logger import api_logger

logger = api_logger.get()


class CachedOpenAIEmbeddings(OpenAIEmbeddings):
    use_local_cache: bool = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object.__setattr__(self, "_cache", {})
        object.__setattr__(self, "_embeddings_cache_filename", settings.get().COPILOT_NAME + "_embeddings_cache.pkl")
        self._load_local_cache()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if self.use_local_cache:
            return self._embed_documents_cached(texts)
        return super().embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        return super().embed_query(text)

    def _embed_documents_cached(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            text_hash = self._hash(text)
            if embedding := self._cache.get(text_hash):
                embeddings.append(embedding)
            else:
                embedding = super().embed_documents([text])[0]
                self._cache[text_hash] = embedding
                embeddings.append(embedding)
        return embeddings

    def _hash(self, text) -> str:
        return xxhash.xxh64(text.encode("utf-8")).hexdigest()

    def _load_local_cache(self):
        try:
            with open(self._embeddings_cache_filename, "rb") as f:
                data = pickle.load(f)
                object.__setattr__(self, "_cache", data)
        except:
            pass

    def save_local_cache(self):
        if self.use_local_cache:
            try:
                with open(self._embeddings_cache_filename, "wb") as f:
                    pickle.dump(self._cache, f)
            except Exception as e:
                logger.warning(f"Failed to save embeddings cache to {self._embeddings_cache_filename}")


def execute(use_local_cache: bool = False):
    openai_api_base = None
    headers = None
    if settings.get().HELICONE_API_KEY:
        openai_api_base = settings.get().HELICONE_BASE_URL
        headers = {
            "Helicone-Auth": "Bearer " + settings.get().HELICONE_API_KEY,
            "Helicone-Cache-Enabled": "true",
        }
    return CachedOpenAIEmbeddings(
        disallowed_special=(), use_local_cache=use_local_cache,
        openai_api_base=openai_api_base,
        headers=headers
    )
