import os
import platform
from dataclasses import dataclass
from typing import Any
from typing import List
from typing import Tuple
from typing import Optional
from typing_extensions import Annotated, TypedDict

import typer
import psutil
import requests
from pydantic import BaseModel, Field
from tqdm import tqdm
from rich.console import Console
from rich.table import Table
from rich import print
from fastapi import APIRouter
from fastapi import Depends

console = Console()

oss_app = typer.Typer(
    name="oss",
    help="OpenCopilot tool to manage and interact with Open Source LLMs.",
    no_args_is_help=True,
)

MODEL_PATH = "models/"

LLAMA_PROMPT_TEMPLATE = "[INST] <<SYS>>\nYou are a helpful ... {prompt}[/INST]"


@dataclass
class ModelInfo:
    name: str
    size: float
    description: str
    prompt_template: str
    filename: str
    url: str
    context_size: int


class Tokens(TypedDict):
    prompt_tokens: List[int]


class TokenizeRequest(BaseModel):
    prompt: str = Field(
        default="", description="The prompt to generate completions for."
    )


MODELS = {
    "Llama-2-7b-chat": ModelInfo(
        name="llama-2-7b-chat",
        size=3.83,
        description="Meta developed and publicly released the Llama 2 family of large language models (LLMs), a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. Fine-tuned LLMs, called Llama-2-Chat, are optimized for dialogue use cases.",
        prompt_template=LLAMA_PROMPT_TEMPLATE,
        filename="llama-2-7b-chat.Q4_0.gguf",
        context_size=4096,
        url="https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_0.gguf",
    ),
    "Llama-2-13b-chat": ModelInfo(
        name="Llama-2-13b-chat",
        size=7.37,
        description="Meta developed and publicly released the Llama 2 family of large language models (LLMs), a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. Fine-tuned LLMs, called Llama-2-Chat, are optimized for dialogue use cases.",
        prompt_template=LLAMA_PROMPT_TEMPLATE,
        filename="llama-2-13b-chat.Q4_0.gguf",
        context_size=4096,
        url="https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q4_0.gguf",
    ),
    "Llama-2-70b-chat": ModelInfo(
        name="Llama-2-70b-chat",
        size=38.9,
        description="Meta developed and publicly released the Llama 2 family of large language models (LLMs), a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. Fine-tuned LLMs, called Llama-2-Chat, are optimized for dialogue use cases.",
        prompt_template=LLAMA_PROMPT_TEMPLATE,
        filename="llama-2-70b-chat.Q4_0.gguf",
        context_size=4096,
        url="https://huggingface.co/TheBloke/Llama-2-70B-chat-GGUF/resolve/main/llama-2-70b-chat.Q4_0.gguf",
    ),
    "CodeLlama-7b": ModelInfo(
        name="CodeLlama-7b",
        size=3.83,
        description="Code Llama is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 34 billion parameters. This model is designed for general code synthesis and understanding.",
        prompt_template="None",
        filename="codellama-7b.Q4_0.gguf",
        context_size=4096,
        url="https://huggingface.co/TheBloke/CodeLlama-7B-GGUF/resolve/main/codellama-7b.Q4_0.gguf",
    ),
    "CodeLlama-13b": ModelInfo(
        name="CodeLlama-13b",
        size=7.37,
        description="Code Llama is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 34 billion parameters. This model is designed for general code synthesis and understanding.",
        prompt_template="None",
        filename="codellama-13b.Q4_0.gguf",
        context_size=4096,
        url="https://huggingface.co/TheBloke/CodeLlama-7B-GGUF/resolve/main/codellama-13b.Q4_0.gguf",
    ),
    "CodeLlama-34b": ModelInfo(
        name="CodeLlama-34b",
        size=19.1,
        description="Code Llama is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 34 billion parameters. This model is designed for general code synthesis and understanding.",
        prompt_template="None",
        filename="codellama-34b.Q4_0.gguf",
        context_size=4096,
        url="https://huggingface.co/TheBloke/CodeLlama-34B-GGUF/resolve/main/codellama-34b.Q4_0.gguf",
    ),
}


def _is_macos() -> bool:
    return platform.system() == "Darwin"


def _can_use_model(model: ModelInfo) -> bool:
    total_memory = psutil.virtual_memory().total / (1024**3)
    return model.size < total_memory / 2


def _is_model_installed(model: ModelInfo) -> bool:
    return os.path.exists(os.path.join(MODEL_PATH, model.filename))


def _remove_model(model: ModelInfo) -> bool:
    return os.remove(os.path.join(MODEL_PATH, model.filename))


def _download_model(url: str, filename: str):
    model_file_path = os.path.join(MODEL_PATH, filename)
    if os.path.exists(model_file_path):
        resume_byte = os.path.getsize(model_file_path)
    else:
        resume_byte = 0

    headers = {}
    if resume_byte:
        headers["Range"] = f"bytes={resume_byte}-"

    response = requests.get(url, headers=headers, stream=True)

    total_size = resume_byte + int(response.headers.get("content-length", 0))
    progress_bar = tqdm(
        total=total_size, unit="B", unit_scale=True, initial=resume_byte
    )

    os.makedirs(MODEL_PATH, exist_ok=True)
    with open(model_file_path, "ab" if resume_byte else "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            progress_bar.update(len(chunk))
    progress_bar.close()


def _try_llama_cpp_imports() -> Optional[Tuple[Any, ...]]:
    # pylint: disable=import-error
    try:
        import uvicorn
        import llama_cpp
        from llama_cpp.server.app import create_app, Settings, get_llama, router

        return uvicorn, llama_cpp, create_app, Settings, get_llama, router
    except:
        print(
            "Could not run LLM, make sure you've installed [code]llama-cpp-python[/code] package and dependencies!"
        )
        if _is_macos():
            print(
                'To install: [code]CMAKE_ARGS="-DLLAMA_METAL=on" pip install \"llama-cpp-python[server]\" pydantic_settings sse_starlette[/code]'
            )
        else:
            print(
                "To install: [code]pip install \"llama-cpp-python[server]\" pydantic_settings sse_starlette[/code]"
            )
        print(
            "More information on how to install: [link]https://llama-cpp-python.readthedocs.io/en/latest/#installation[/link]"
        )
        print("Re-run this command after installation is done!")
        return None


def _define_tokenize_route(router: APIRouter, llama_cpp: Any, get_llama: Any):
    @router.post("/v1/tokenize")
    async def tokenize(
        body: TokenizeRequest,
        llama: llama_cpp.Llama = Depends(get_llama),
    ) -> Tokens:
        try:
            tokens = llama.tokenize(text=body.prompt.encode("utf-8"), add_bos=True)
        except Exception as e:
            print(f'Error while tokenizing "{body.prompt}": {e}')
        return {"prompt_tokens": tokens}


@oss_app.command("list")
def list_models():
    """List available open source large language models"""
    table = Table(
        "",
        "NAME",
        "SIZE",
        "INSTALLED",
    )
    for model_name, model in MODELS.items():
        table.add_row(
            "*" if _can_use_model(model) else "",
            model_name,
            f"{model.size}GB",
            "Yes" if _is_model_installed(model) else "No",
        )
    console.print(table)
    print("\n* Recommended for your system")
    print(
        "\nTo see more details about a model: [code]opencopilot oss info <model_name>[/code]"
    )


@oss_app.command("info")
def model_info(model_name: str):
    try:
        model = MODELS.get(model_name)
        table = Table(show_header=False, box=None)
        table.add_column("Label", no_wrap=True, style="bold")
        table.add_column("Value")
        table.add_row("Model Name:", model.name)
        table.add_row("Size:", f"{model.size} GB")
        table.add_row("Description:", model.description)
        console.print(table)
    except:
        typer.echo(f"Model {model_name} not found!")


@oss_app.command("remove")
def model_remove(model_name: str):
    model = MODELS.get(model_name)
    if not model:
        typer.echo(f"Model {model_name} not found!")
        return
    if _is_model_installed(model):
        _remove_model(model)
        print(f"LLM [bold]{model.name}[/bold] removed successfully.")
    else:
        print(f"[bold]{model.name}[/bold] not downloaded - nothing to remove.")


@oss_app.command("run")
def run_model(model_name: Annotated[str, typer.Argument(...)] = "Llama-2-7b-chat"):
    """Run a specific model."""
    model = MODELS.get(model_name)
    if not model:
        typer.echo(f"Model {model_name} not found!")
        return
    try:
        typer.echo(f"Downloading {model_name}...")
        _download_model(model.url, model.filename)
        typer.echo(f"Running {model.name}...")
    except:
        typer.echo(f"Could not run {model_name}!")

    modules = _try_llama_cpp_imports()
    if not modules:
        return

    uvicorn, llama_cpp, create_app, Settings, get_llama, router = modules
    _define_tokenize_route(router, llama_cpp, get_llama)

    settings = Settings(
        model=os.path.join(MODEL_PATH, model.filename),
        n_ctx=model.context_size,
        n_gpu_layers=1,
        use_mlock=True,
    )

    app = create_app(settings=settings)
    uvicorn.run(
        app,
        host=os.getenv("OSS_LLM_HOST", "localhost"),
        port=int(os.getenv("OSS_LLM_PORT", 8000)),
    )


@oss_app.command("prompt")
def generate_prompt(model_name: str):
    """Generate a model-specific prompt template."""
    if model_name in MODELS:
        typer.echo(MODELS[model_name].prompt_template)
    else:
        typer.echo(f"No prompt template available for {model_name}!")
