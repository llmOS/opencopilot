from typing import List
from typing import Optional

import tqdm
import weaviate
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import TextSplitter
from langchain.vectorstores import Weaviate
from requests.exceptions import ConnectionError
from requests.exceptions import InvalidSchema
from requests.exceptions import MissingSchema
from weaviate import UnexpectedStatusCodeException
from weaviate import WeaviateStartUpError
from weaviate.exceptions import WeaviateBaseError

from opencopilot import settings
from opencopilot.domain import error_messages
from opencopilot.domain.errors import WeaviateRuntimeError
from opencopilot.utils import get_embedding_model_use_case
from opencopilot.utils.get_embedding_model_use_case import CachedOpenAIEmbeddings


class DocumentStore:
    document_embed_model = "text-embedding-ada-002"
    document_chunk_size = 2000

    def get_embeddings_model(self) -> CachedOpenAIEmbeddings:
        return get_embedding_model_use_case.execute(use_local_cache=True)

    def get_text_splitter(self) -> TextSplitter:
        return CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.document_chunk_size,
            model_name=self.document_embed_model,
            separator=" ",
            disallowed_special=(),
        )

    def ingest_data(self, documents: List[Document]):
        pass

    def find(self, query: str, **kwargs) -> List[Document]:
        return []


class WeaviateDocumentStore(DocumentStore):
    ingest_batch_size = 100

    weaviate_index_name = "LangChain"  # TODO: Weaviate specific?

    def __init__(self):
        self.documents = []
        self.embeddings = self.get_embeddings_model()
        self.weaviate_client = self._get_weaviate_client()
        self.vector_store = self._get_vector_store()

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
        except WeaviateStartUpError:
            raise WeaviateRuntimeError(
                error_messages.WEAVIATE_DID_NOT_START.format(
                    weaviate_url=settings.get().WEAVIATE_URL or "http://localhost:8080"
                )
            )
        except WeaviateBaseError as exc:
            raise WeaviateRuntimeError(exc.message)

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
            print(
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
        except ConnectionError:
            raise WeaviateRuntimeError(error_messages.WEAVIATE_CONNECTION_ERROR)
        except UnexpectedStatusCodeException:
            raise WeaviateRuntimeError(error_messages.WEAVIATE_QUERY_ERROR)
        except WeaviateBaseError as exc:
            raise WeaviateRuntimeError(exc.message)

    def find(self, query: str, **kwargs) -> List[Document]:
        try:
            kwargs["k"] = kwargs.get("k", settings.get().MAX_CONTEXT_DOCUMENTS_COUNT)
            documents = self.vector_store.similarity_search(query, **kwargs)
            return documents
        except ConnectionError:
            raise WeaviateRuntimeError(error_messages.WEAVIATE_CONNECTION_ERROR)
        except UnexpectedStatusCodeException:
            raise WeaviateRuntimeError(error_messages.WEAVIATE_QUERY_ERROR)
        except WeaviateBaseError as exc:
            raise WeaviateRuntimeError(exc.message)

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
        except ConnectionError:
            raise WeaviateRuntimeError(error_messages.WEAVIATE_CONNECTION_ERROR)
        except UnexpectedStatusCodeException:
            raise WeaviateRuntimeError(error_messages.WEAVIATE_QUERY_ERROR)
        except WeaviateBaseError as exc:
            raise WeaviateRuntimeError(exc.message)

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
        except ConnectionError:
            raise WeaviateRuntimeError(error_messages.WEAVIATE_CONNECTION_ERROR)
        except UnexpectedStatusCodeException:
            raise WeaviateRuntimeError(error_messages.WEAVIATE_QUERY_ERROR)
        except WeaviateBaseError as exc:
            raise WeaviateRuntimeError(exc.message)


class EmptyDocumentStore(DocumentStore):
    pass


DOCUMENT_STORE = Optional[DocumentStore]


def init_document_store(document_store: DocumentStore):
    global DOCUMENT_STORE
    DOCUMENT_STORE = document_store


def get_document_store() -> DocumentStore:
    return DOCUMENT_STORE
