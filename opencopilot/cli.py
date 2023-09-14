import logging
import os
import uuid
from contextlib import nullcontext
from typing import Optional
from enum import Enum

import typer
from rich.console import Console
from rich.table import Table
from rich import print as rich_print
from rich.prompt import Prompt
from typing_extensions import Annotated

from opencopilot import exception_utils
from opencopilot.domain.cli import cli_chat_use_case
from opencopilot.logger import api_logger
from opencopilot.utils.scripting import set_default_settings

from opencopilot.oss import oss_app
from opencopilot.utils.validators import validate_openai_api_key
from opencopilot.utils.prompting import generate_prompt
from opencopilot.utils.prompting import (
    GPT_PROMPT_SUFFIX,
    LLAMA_2_PROMPT_PREFIX,
    LLAMA_2_PROMPT_SUFFIX,
)


class ModelType(str, Enum):
    gpt = "gpt"
    llama2 = "llama2"


logger = api_logger.get()
logger.setLevel(logging.WARNING)
console = Console()

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    pretty_exceptions_enable=False,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_short=False,
)

exception_utils.add_copilot_exception_catching()
app.add_typer(oss_app, name="oss")


@app.callback()
def main(ctx: typer.Context):
    # Initialize settings
    set_default_settings("cli")


@app.command(help="Chat with the Copilot. Example: chat 'Hello, who are you?'")
def chat(message: str):
    print("Message:", message)
    conversation_id = uuid.uuid4()
    while message:
        print("Response: ", end="", flush=True)
        cli_chat_use_case.conversation_stream(
            base_url="http://0.0.0.0:3000",
            conversation_id=conversation_id,
            message=message,
            stream=True,
        )
        print()
        message = input("Message: ")


@app.command(
    help="Generate a prompt. Example: prompt 'Copilot for teaching children mathematics'"
)
def prompt(
    description: str = typer.Argument(..., help="Copilot description"),
    model: ModelType = typer.Option(
        "gpt",
        "--model",
        help="Produce prompt suitable for the specified model.",
    ),
):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    while True:
        try:
            validate_openai_api_key(openai_api_key)
            break
        except:
            openai_api_key = Prompt.ask(
                "[yellow]For prompt generation, your OpenAI API key is required. Please type it in below:[/yellow]\n"
            )
            os.environ["OPENAI_API_KEY"] = openai_api_key
    rich_print(
        f'[bold]Generating {"GPT-style prompt" if model == ModelType.gpt else "LLama-2 style"} template for "{description}"[/bold]:'
    )
    if model == ModelType.llama2:
        print(LLAMA_2_PROMPT_PREFIX)
    prompt = generate_prompt(description)
    print(GPT_PROMPT_SUFFIX if model == ModelType.gpt else LLAMA_2_PROMPT_SUFFIX)
    print()


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
    openai_api_key = os.getenv("OPENAI_API_KEY")
    validate_openai_api_key(openai_api_key)

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
