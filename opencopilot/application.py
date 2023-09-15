import os
from datetime import timedelta
from typing import Callable
from typing import List
from typing import Optional
from typing import Union

import uvicorn
from fastapi import APIRouter
from langchain.chat_models.base import BaseChatModel
from langchain.embeddings.base import Embeddings
from langchain.schema import Document

from opencopilot import exception_utils
from opencopilot import settings
from opencopilot.analytics import TrackingEventType
from opencopilot.analytics import track
from opencopilot.domain import error_messages
from opencopilot.domain.chat.models.local import LocalLLM
from opencopilot.domain.errors import LogsDirError
from opencopilot.domain.errors import ModelError
from opencopilot.logger import api_logger
from opencopilot.repository.documents import split_documents_use_case
from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)
from opencopilot.repository.users_repository import UsersRepositoryLocal
from opencopilot.settings import Settings
from opencopilot.utils.validators import validate_local_llm
from opencopilot.utils.validators import validate_openai_api_key
from opencopilot.utils.validators import validate_prompt_and_prompt_file_config
from opencopilot.utils.validators import validate_system_prompt
from opencopilot.callbacks import CopilotCallbacks
from opencopilot.callbacks import PromptBuilder

ALLOWED_LLM_MODEL_NAMES = ["gpt-3.5-turbo-16k", "gpt-4"]

exception_utils.add_copilot_exception_catching()


class OpenCopilot:
    def __init__(
        self,
        prompt: Optional[str] = None,
        prompt_file: Optional[str] = None,
        question_template: Optional[str] = "### Human: {question}",
        response_template: Optional[str] = "### Assistant: {response}",
        openai_api_key: Optional[str] = None,
        copilot_name: str = "default",
        host: str = "127.0.0.1",
        api_port: int = 3000,
        environment: str = "local",
        allowed_origins: str = "*",
        weaviate_url: Optional[str] = None,
        weaviate_read_timeout: int = 120,
        llm: Optional[Union[str, BaseChatModel]] = "gpt-3.5-turbo-16k",
        embedding_model: Optional[Union[str, Embeddings]] = "text-embedding-ada-002",
        max_document_size_mb: int = 50,
        auth_type: Optional[str] = None,
        api_key: Optional[str] = None,
        jwt_client_id: Optional[str] = None,
        jwt_client_secret: Optional[str] = None,
        jwt_token_expiration_seconds: Optional[int] = timedelta(days=1).total_seconds(),
        helicone_api_key: Optional[str] = None,
        helicone_rate_limit_policy: Optional[str] = "3;w=60;s=user",
        logs_dir: Optional[str] = "logs",
        log_level: Optional[Union[str, int]] = None,
    ):
        api_logger.set_log_level(log_level)

        if not openai_api_key:
            openai_api_key = os.getenv("OPENAI_API_KEY")

        tracking_enabled = (
            not os.environ.get("OPENCOPILOT_DO_NOT_TRACK", "").lower() == "true"
        )

        if isinstance(llm, str) or isinstance(embedding_model, str):
            validate_openai_api_key(openai_api_key)
        validate_prompt_and_prompt_file_config(prompt, prompt_file)

        if not prompt:
            with open(prompt_file, "r") as f:
                prompt = f.read()

        validate_system_prompt(prompt)

        if isinstance(llm, str) and llm not in ALLOWED_LLM_MODEL_NAMES:
            raise ModelError(
                error_messages.INVALID_MODEL_ERROR.format(
                    llm_model_name=llm,
                    allowed_model_names=ALLOWED_LLM_MODEL_NAMES,
                )
            )
        if isinstance(llm, LocalLLM):
            validate_local_llm(llm)

        if not logs_dir:
            raise LogsDirError(error_messages.INVALID_LOGS_DIR_ERROR)

        settings.set(
            Settings(
                PROMPT=prompt,
                QUESTION_TEMPLATE=question_template,
                RESPONSE_TEMPLATE=response_template,
                OPENAI_API_KEY=openai_api_key,
                COPILOT_NAME=copilot_name,
                HOST=host,
                API_PORT=api_port,
                ENVIRONMENT=environment,
                ALLOWED_ORIGINS=allowed_origins,
                WEAVIATE_URL=weaviate_url,
                WEAVIATE_READ_TIMEOUT=weaviate_read_timeout,
                LLM=llm,
                EMBEDDING_MODEL=embedding_model,
                MAX_DOCUMENT_SIZE_MB=max_document_size_mb,
                AUTH_TYPE=auth_type,
                API_KEY=api_key,
                JWT_CLIENT_ID=jwt_client_id,
                JWT_CLIENT_SECRET=jwt_client_secret,
                JWT_TOKEN_EXPIRATION_SECONDS=jwt_token_expiration_seconds,
                HELICONE_API_KEY=helicone_api_key,
                HELICONE_RATE_LIMIT_POLICY=helicone_rate_limit_policy,
                TRACKING_ENABLED=tracking_enabled,
                LOGS_DIR=logs_dir,
            )
        )

        self.llm = llm
        self.embedding_model = embedding_model
        self.host = host
        self.api_port = api_port
        self.data_loaders = []
        self.local_files_dirs = []
        self.data_urls = []
        self.local_file_paths = []
        self.documents = []
        self.callbacks = CopilotCallbacks()
        self.router = _get_custom_router()

    def __call__(self, *args, **kwargs):
        from .repository.documents import document_loader
        from .repository.documents import document_store
        from opencopilot.repository.documents.document_store import (
            WeaviateDocumentStore,
        )
        from opencopilot.repository.documents.document_store import EmptyDocumentStore
        from opencopilot.utils.loaders import urls_loader
        from opencopilot.logger import api_logger

        logger = api_logger.get()

        if (
            self.data_loaders
            or self.local_files_dirs
            or self.local_file_paths
            or self.data_urls
        ):
            self.document_store = WeaviateDocumentStore()
            if settings.get().WEAVIATE_URL:
                logger.info("Connected to Weaviate vector DB.")
            else:
                logger.info("Running embedded Weaviate vector DB.")
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

        self.chat_history_repository = ConversationHistoryRepositoryLocal()
        self.users_repository = UsersRepositoryLocal()

        from .app import app

        app.copilot_callbacks = self.callbacks
        app.include_router(self.router)
        track(
            TrackingEventType.COPILOT_START,
            len(self.documents),
            len(self.data_loaders),
            len(self.local_files_dirs),
            len(self.local_file_paths),
            len(self.data_urls),
        )

        uvicorn.run(
            app,
            host=self.host,
            port=self.api_port,
            log_level=api_logger.get().level,
        )

    def data_loader(self, function: Callable[[], Document]):
        self.data_loaders.append(function)
        return function

    def add_local_files_dir(self, files_dir: str) -> None:
        self.local_files_dirs.append(files_dir)

    def add_data_urls(self, urls: List[str]) -> None:
        self.data_urls.extend(urls)

    def prompt_builder(self, function: PromptBuilder):
        self.callbacks.prompt_builder = function
        return function


def _get_custom_router() -> APIRouter:
    router = APIRouter()
    router.openapi_tags = ["Custom"]
    router.title = "Custom router"
    return router
