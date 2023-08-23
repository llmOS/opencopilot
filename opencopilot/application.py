import os
from datetime import timedelta
from typing import Callable
from typing import Literal
from typing import Optional

import uvicorn
from langchain.schema import Document

from . import settings
from .settings import Settings


class OpenCopilot:
    def __init__(
        self,
        prompt_file: str,
        openai_api_key: Optional[str] = None,
        copilot_name: str = "default",
        host: str = "127.0.0.1",
        api_base_url: str = "http://127.0.0.1/",
        api_port: int = 3000,
        environment: str = "local",
        allowed_origins: str = "*",
        application_name: str = "my-copilot",
        log_file_path="./logs/logs.log",
        weaviate_url: str = "http://localhost:8080/",
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
        assert (
            openai_api_key
        ), "OPENAI_API_KEY must be passed to OpenCopilot or be set in the environment."

        settings.set(
            Settings(
                OPENAI_API_KEY=openai_api_key,
                COPILOT_NAME=copilot_name,
                HOST=host,
                API_PORT=api_port,
                API_BASE_URL=api_base_url,
                ENVIRONMENT=environment,
                ALLOWED_ORIGINS=allowed_origins,
                APPLICATION_NAME=application_name,
                LOG_FILE_PATH=log_file_path,
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
            )
        )

        assert self.add_prompt(prompt_file), "Valid prompt file is required"
        self.host = host
        self.api_port = api_port
        self.data_loaders = []
        self.local_files_dirs = []
        self.local_file_paths = []
        self.documents = []

    def __call__(self, *args, **kwargs):
        from .repository.documents import document_loader
        from .repository.documents import document_store
        from opencopilot.repository.documents.document_store import (
            WeaviateDocumentStore,
        )
        from opencopilot.repository.documents.document_store import EmptyDocumentStore

        if self.data_loaders or self.local_files_dirs or self.local_file_paths:
            self.document_store = WeaviateDocumentStore()
        else:
            self.document_store = EmptyDocumentStore()
        document_store.init_document_store(self.document_store)

        for data_loader in self.data_loaders:
            self.documents.extend(data_loader())

        for data_dir in self.local_files_dirs:
            text_splitter = self.document_store.get_text_splitter()
            self.documents.extend(
                document_loader.execute(data_dir, False, text_splitter)
            )

        if self.documents:
            self.document_store.ingest_data(self.documents)

        from .app import app

        uvicorn.run(app, host=self.host, port=self.api_port)

    @staticmethod
    def add_prompt(prompt_file: str) -> bool:
        return settings.init_prompt_file_location(prompt_file)

    def data_loader(self, function: Callable[[], Document]):
        self.data_loaders.append(function)

    def add_local_files_dir(self, files_dir: str) -> None:
        self.local_files_dirs.append(files_dir)

    # def add_local_file(self, file_path: str) -> None:
    #    self.local_file_paths.append(file_path)
