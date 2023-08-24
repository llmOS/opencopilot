import os
import uuid

import typer
from rich.console import Console
from rich.table import Table

from opencopilot import settings
from opencopilot.settings import Settings
from opencopilot.scripts import chat as chat_script

console = Console()

app = typer.Typer(add_completion=False, no_args_is_help=True)


def _set_settings():
    settings.set(
        Settings(
            COPILOT_NAME="cli",
            HOST="127.0.0.1",
            API_PORT=3000,
            API_BASE_URL="http://localhost:3000/",
            ENVIRONMENT="cli",
            ALLOWED_ORIGINS="*",
            APPLICATION_NAME="cli",
            LOG_FILE_PATH="./logs/cli.log",
            WEAVIATE_URL="http://localhost:8080/",
            WEAVIATE_READ_TIMEOUT=120,
            MODEL="gpt-4",
            OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"),
            MAX_DOCUMENT_SIZE_MB=1,
            SLACK_WEBHOOK="",
            AUTH_TYPE=None,
            API_KEY="",
            JWT_CLIENT_ID="",
            JWT_CLIENT_SECRET="",
            JWT_TOKEN_EXPIRATION_SECONDS=1,
            HELICONE_API_KEY="",
            HELICONE_RATE_LIMIT_POLICY="",
        )
    )


@app.command(help="Print info")
def info():
    print(
        "OpenCopilot CLI. Currently just a convenience layer for chatting with the "
        "copilot."
    )


@app.command(help="Chat with the Copilot. Example: chat 'Hello, who are you?'")
def chat(message: str):
    print("Message:", message)
    conversation_id = uuid.uuid4()
    while message:
        print("Response: ", end="", flush=True)
        chat_script.conversation_stream(
            base_url="http://0.0.0.0:3000",
            conversation_id=conversation_id,
            message=message,
            stream=True,
        )
        print()
        message = input("Message: ")


@app.command(help="Query the retrieval pipeline")
def retrieve(query: str):
    _set_settings()
    from opencopilot.repository.documents.document_store import WeaviateDocumentStore

    document_store = WeaviateDocumentStore()
    documents = document_store.find(query)
    print("Retrieved documents:")
    for document in documents:
        print(f"\t{document.metadata.get('source')}")


@app.command(help="Check if document was ingested")
def is_ingested(source: str):
    import weaviate

    source_client = weaviate.Client(
        url="http://localhost:8080/",  # Replace with your endpoint
    )

    query = (
        source_client.query.get("LangChain", ["source"])
        .with_additional(["id"])
        .with_where(
            {"path": ["source"], "operator": "Like", "valueString": f"*{source}*"}
        )
    )
    document_chunks = query.do().get("data", {}).get("Get", {}).get("LangChain", [])
    documents = {}
    for chunk in document_chunks:
        source = chunk.get("source")
        if source:
            documents[source] = documents.get(source, 0) + 1
    print(f"Found {len(document_chunks)} chunks from {len(documents)} documents:")
    table = Table("Source", "Chunks")
    for source in documents.keys():
        table.add_row(source, str(documents[source]))
    console.print(table)


if __name__ == "__main__":
    app()
