import os
import uuid
from typing import Optional
from contextlib import nullcontext

import typer
from typing_extensions import Annotated
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


@app.command(help="Query the retrieval pipeline.")
def retrieve(
    ctx: typer.Context,
    text: Annotated[
        Optional[str],
        typer.Option(
            "--text", "-t", help='Your question, i.e. "How to improve retrieval?"'
        ),
    ] = None,
    source: Annotated[
        Optional[str],
        typer.Option("--source", "-s", help="Source to match - supports wildcards"),
    ] = None,
    all: Annotated[
        Optional[bool], typer.Option("--all", "-a", help="Gets all documents ingested")
    ] = False,
):
    _set_settings()
    from opencopilot.repository.documents.document_store import WeaviateDocumentStore

    document_store = WeaviateDocumentStore()

    if text is not None:
        where_filter = (
            {"path": ["source"], "operator": "Like", "valueString": source}
            if source
            else None
        )
        document_chunks = document_store.find(text, where_filter=where_filter)
    elif source is not None:
        document_chunks = document_store.find_by_source(source)
    elif all:
        document_chunks = document_store.get_all()
    else:
        typer.echo(ctx.get_help())
        raise typer.Exit()

    documents = {}
    for chunk in document_chunks:
        source = chunk.metadata.get("source")
        if source:
            documents[source] = documents.get(source, 0) + 1

    table = Table("Source", "Chunks")
    for source in documents.keys():
        table.add_row(source, str(documents[source]))

    with nullcontext() if len(documents) < 50 else console.pager():
        console.print(table)
    print(f"{len(documents)} documents in {len(document_chunks)} chunks")


if __name__ == "__main__":
    app()
