import os
from datetime import timedelta
from typing import Callable
from typing import List
from typing import Literal
from typing import Optional

import uvicorn
from langchain.schema import Document

from .repository.documents import split_documents_use_case
from .utils.validators import (
    validate_openai_api_key,
    validate_prompt_and_prompt_file_config,
    validate_system_prompt,
)
from . import settings
from .settings import Settings

from .analytics import track
from .analytics import TrackingEventType


class OpenCopilot:
    def __init__(
        self,
        prompt: Optional[str] = None,
        prompt_file: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        copilot_name: str = "default",
        host: str = "127.0.0.1",
        api_base_url: str = "http://127.0.0.1/",
        api_port: int = 3000,
        environment: str = "local",
        allowed_origins: str = "*",
        weaviate_url: Optional[str] = None,
        weaviate_read_timeout: int = 120,
        llm_model_name: Literal["gpt-3.5-turbo-16k", "gpt-4"] = "gpt-4",
        max_document_size_mb: int = 50,
        slack_webhook: str = "",
        auth_type: Optional[str] = None,
        api_key: str = "",
        jwt_client_id: str = "",
        jwt_client_secret: str = "",
        jwt_token_expiration_seconds: int = timedelta(days=1).total_seconds(),
        helicone_api_key: str = "",
        helicone_rate_limit_policy: str = "3;w=60;s=user",
    ):
        if not openai_api_key:
            openai_api_key = os.getenv("OPENAI_API_KEY")

        tracking_enabled = (
            not os.environ.get("OPENCOPILOT_DO_NOT_TRACK", "").lower() == "true"
        )

        validate_openai_api_key(openai_api_key)
        validate_prompt_and_prompt_file_config(prompt, prompt_file)

        if not prompt:
            with open(prompt_file, "r") as f:
                prompt = f.read()

        validate_system_prompt(prompt)

        settings.set(
            Settings(
                PROMPT=prompt,
                OPENAI_API_KEY=openai_api_key,
                COPILOT_NAME=copilot_name,
                HOST=host,
                API_PORT=api_port,
                API_BASE_URL=api_base_url,
                ENVIRONMENT=environment,
                ALLOWED_ORIGINS=allowed_origins,
                WEAVIATE_URL=weaviate_url,
                WEAVIATE_READ_TIMEOUT=weaviate_read_timeout,
                MODEL=llm_model_name,
                MAX_DOCUMENT_SIZE_MB=max_document_size_mb,
                SLACK_WEBHOOK=slack_webhook,
                AUTH_TYPE=auth_type,
                API_KEY=api_key,
                JWT_CLIENT_ID=jwt_client_id,
                JWT_CLIENT_SECRET=jwt_client_secret,
                JWT_TOKEN_EXPIRATION_SECONDS=jwt_token_expiration_seconds,
                HELICONE_API_KEY=helicone_api_key,
                HELICONE_RATE_LIMIT_POLICY=helicone_rate_limit_policy,
                TRACKING_ENABLED=tracking_enabled,
            )
        )

        self.host = host
        self.api_port = api_port
        self.data_loaders = []
        self.local_files_dirs = []
        self.data_urls = []
        self.local_file_paths = []
        self.documents = []

    def __call__(self, *args, **kwargs):
        from .repository.documents import document_loader
        from .repository.documents import document_store
        from opencopilot.repository.documents.document_store import (
            WeaviateDocumentStore,
        )
        from opencopilot.repository.documents.document_store import EmptyDocumentStore
        from .src.utils.loaders import urls_loader

        if (
            self.data_loaders
            or self.local_files_dirs
            or self.local_file_paths
            or self.data_urls
        ):
            self.document_store = WeaviateDocumentStore()
        else:
            self.document_store = EmptyDocumentStore()
        document_store.init_document_store(self.document_store)

        text_splitter = self.document_store.get_text_splitter()
        for data_loader in self.data_loaders:
            documents = data_loader()
            document_chunks = split_documents_use_case.execute(text_splitter, documents)
            self.documents.extend(document_chunks)

        for data_dir in self.local_files_dirs:
            self.documents.extend(
                document_loader.execute(data_dir, False, text_splitter)
            )

        if len(self.data_urls):
            self.documents.extend(
                urls_loader.execute(
                    self.data_urls, text_splitter, settings.get().MAX_DOCUMENT_SIZE_MB
                )
            )

        if self.documents:
            self.document_store.ingest_data(self.documents)

        from .app import app

        track(
            TrackingEventType.COPILOT_START,
            len(self.documents),
            len(self.data_loaders),
            len(self.local_files_dirs),
            len(self.local_file_paths),
            len(self.data_urls),
        )

        uvicorn.run(app, host=self.host, port=self.api_port)

    def data_loader(self, function: Callable[[], Document]):
        self.data_loaders.append(function)

    def add_local_files_dir(self, files_dir: str) -> None:
        self.local_files_dirs.append(files_dir)

    def add_data_urls(self, urls: List[str]) -> None:
        self.data_urls.extend(urls)

    # def add_local_file(self, file_path: str) -> None:
    #    self.local_file_paths.append(file_path)
