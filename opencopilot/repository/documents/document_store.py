from typing import List
from typing import Optional

import tqdm
import weaviate
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import TextSplitter
from langchain.vectorstores import Weaviate
from requests.exceptions import InvalidSchema
from requests.exceptions import MissingSchema
from weaviate.exceptions import WeaviateBaseError

from opencopilot import settings
from opencopilot.domain import error_messages
from opencopilot.domain.errors import WeaviateRuntimeError
from opencopilot.logger import api_logger
from opencopilot.utils import get_embedding_model_use_case
from opencopilot.utils.get_embedding_model_use_case import CachedEmbeddings
from opencopilot.utils.stdout import ignore_stdout

logger = api_logger.get()


class DocumentStore:
    """
    A store for managing and retrieving documents using embeddings.

    This class provides mechanisms to ingest documents, fetch embeddings, and perform
    search queries. It can leverage different embedding models, with a default model provided.

    Attributes:
        document_embed_model (str): The default embedding model identifier.
        document_chunk_size (int): Size of text chunks for embeddings. Defaults to 2000 but may be smaller
                                   depending on the embedding model.
    """

    document_embed_model = "text-embedding-ada-002"
    document_chunk_size = 2000

    def __init__(self):
        """
        Initialize the DocumentStore, setting the document chunk size based on the embedding model in use.
        """
        embeddings = settings.get().EMBEDDING_MODEL
        if not isinstance(embeddings, str):
            # smaller chunks if not using OpenAI
            self.document_chunk_size = 500

    def get_embeddings_model(self) -> CachedEmbeddings:
        """
        Fetch the embeddings model currently in use.

        Returns:
            CachedEmbeddings: The embeddings model object.
        """
        return get_embedding_model_use_case.execute()

    def get_text_splitter(self) -> TextSplitter:
        """
        Retrieve a text splitter configured for the current embedding model and chunk size.

        Returns:
            TextSplitter: An instance of a text splitter utility.
        """
        return RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.document_chunk_size,
            model_name=self.document_embed_model,
            disallowed_special=(),
        )

    def ingest_data(self, documents: List[Document]):
        """
        Ingest a list of documents into the store.

        Args:
            documents (List[Document]): A list of Document objects to be ingested.

        Returns:
            None
        """
        pass

    def find(self, query: str, **kwargs) -> List[Document]:
        """
        Search for documents that match the provided query.

        Args:
            query (str): The search query string.
            **kwargs: Additional search parameters, if any.

        Returns:
            List[Document]: A list of Document objects matching the query.
        """
        return []


class WeaviateDocumentStore(DocumentStore):
    ingest_batch_size = 100

    weaviate_index_name = "LangChain"  # TODO: Weaviate specific?

    def __init__(self):
        super().__init__()
        self.documents = []
        self.embeddings = self.get_embeddings_model()
        self.weaviate_client = self._get_weaviate_client()
        self.vector_store = self._get_vector_store()

    @ignore_stdout
    def _get_weaviate_client(self):
        try:
            if url := settings.get().WEAVIATE_URL:
                return weaviate.Client(
                    url=url,
                    timeout_config=(10, settings.get().WEAVIATE_READ_TIMEOUT),
                )
            else:
                return weaviate.Client(
                    timeout_config=(10, settings.get().WEAVIATE_READ_TIMEOUT),
                    embedded_options=weaviate.embedded.EmbeddedOptions(
                        port=8080,
                        hostname="localhost",
                    ),
                )
        except WeaviateBaseError as exc:
            raise WeaviateRuntimeError(
                exc.message + error_messages.WEAVIATE_ERROR_EXTRA
            )
        except MissingSchema:
            raise WeaviateRuntimeError(
                error_messages.WEAVIATE_INVALID_URL.format(
                    weaviate_url=settings.get().WEAVIATE_URL or "http://localhost:8080"
                )
            )
        except InvalidSchema:
            raise WeaviateRuntimeError(
                error_messages.WEAVIATE_INVALID_URL.format(
                    weaviate_url=settings.get().WEAVIATE_URL or "http://localhost:8080"
                )
            )

    def _get_vector_store(self):
        metadatas = [d.metadata for d in self.documents]
        attributes = list(metadatas[0].keys()) if metadatas else ["source"]
        return Weaviate(
            self.weaviate_client,
            index_name=self.weaviate_index_name,
            text_key="text",
            embedding=self.embeddings,
            attributes=attributes,
            by_text=False,
        )

    def ingest_data(self, documents: List[Document]):
        try:
            self.documents = documents
            batch_size = self.ingest_batch_size
            logger.info(
                f"Got {len(documents)} documents, embedding with batch "
                f"size: {batch_size}"
            )
            self.weaviate_client.schema.delete_all()

            for i in tqdm.tqdm(
                range(0, int(len(documents) / batch_size) + 1), desc="Embedding.."
            ):
                batch = documents[i * batch_size : (i + 1) * batch_size]
                self.vector_store.add_documents(batch)

            self.embeddings.save_local_cache()
            self.vector_store = self._get_vector_store()
        except WeaviateBaseError as exc:
            raise WeaviateRuntimeError(
                exc.message + error_messages.WEAVIATE_ERROR_EXTRA
            )

    def find(self, query: str, **kwargs) -> List[Document]:
        try:
            kwargs["k"] = kwargs.get("k", settings.get().MAX_CONTEXT_DOCUMENTS_COUNT)
            documents = self.vector_store.similarity_search(query, **kwargs)
            return documents
        except WeaviateBaseError as exc:
            raise WeaviateRuntimeError(
                exc.message + error_messages.WEAVIATE_ERROR_EXTRA
            )

    def find_by_source(self, source: str, **kwargs) -> List[Document]:
        try:
            query = (
                self._get_weaviate_client()
                .query.get(self.weaviate_index_name, ["text", "source"])
                .with_additional(["id"])
                .with_where(
                    {"path": ["source"], "operator": "Like", "valueString": source}
                )
            )
            result = (
                query.do()
                .get("data", {})
                .get("Get", {})
                .get(self.weaviate_index_name, [])
            )
            docs = []
            for res in result:
                text = res.pop("text")
                docs.append(Document(page_content=text, metadata=res))
            return docs
        except WeaviateBaseError as exc:
            raise WeaviateRuntimeError(
                exc.message + error_messages.WEAVIATE_ERROR_EXTRA
            )

    def get_all(self) -> List[Document]:
        try:
            client = self._get_weaviate_client()
            batch_size = 200
            cursor = None
            all_results = []

            query = (
                client.query.get(self.weaviate_index_name, ["text", "source"])
                .with_additional(["id"])
                .with_limit(batch_size)
            )

            while True:
                results = query.with_after(cursor).do() if cursor else query.do()
                current_results = results["data"]["Get"].get(
                    self.weaviate_index_name, []
                )
                if not current_results:
                    break
                all_results.extend(current_results)
                cursor = current_results[-1]["_additional"]["id"]

            docs = [
                Document(page_content=res.pop("text"), metadata=res)
                for res in all_results
            ]
            return docs
        except WeaviateBaseError as exc:
            raise WeaviateRuntimeError(
                exc.message + error_messages.WEAVIATE_ERROR_EXTRA
            )


class EmptyDocumentStore(DocumentStore):
    pass


DOCUMENT_STORE = Optional[DocumentStore]


def init_document_store(document_store: DocumentStore):
    global DOCUMENT_STORE
    DOCUMENT_STORE = document_store


def get_document_store() -> DocumentStore:
    return DOCUMENT_STORE
