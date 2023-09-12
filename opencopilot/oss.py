import os
import platform
from dataclasses import dataclass
from typing import Any
from typing import Optional

import typer
import psutil
import requests
from tqdm import tqdm
from rich.console import Console
from rich.table import Table
from rich import print

console = Console()

oss_app = typer.Typer(
    name="oss",
    help="OpenCopilot tool to manage and interact with Open Source LLMs.",
    no_args_is_help=True,
)

MODEL_PATH = os.path.expanduser("~/.opencopilot/models/")

LLAMA_PROMPT_TEMPLATE = """<s>[INST] <<SYS>>\nYour purpose is to repeat what the user says, but in a different wording.\nDon't add anything, don't answer any questions, don't give any advice or comment - just repeat.\nContext:\n{context}\n<</SYS>>\n\n{history} Repeat: {question} [/INST]"""

CODELLAMA_PROMPT_TEMPLATE = "<s>[INST] <<SYS>>\nWrite code to solve the following coding problem that obeys the constraints and passes the example test cases.\nPlease wrap your code answer using ```.\nRelevant information: {context}. \n<</SYS>>\n\n{history} {question} [/INST]"


@dataclass
class ModelInfo:
    name: str
    size: float
    description: str
    prompt_template: str
    filename: str
    url: str
    context_size: int


MODELS = {
    "llama-2-7b-chat": ModelInfo(
        name="llama-2-7b-chat",
        size=3.83,
        description="Meta developed and publicly released the Llama 2 family of large language models (LLMs), a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. Fine-tuned LLMs, called Llama-2-Chat, are optimized for dialogue use cases.",
        prompt_template=LLAMA_PROMPT_TEMPLATE,
        filename="llama-2-7b-chat.Q4_0.gguf",
        context_size=4096,
        url="https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_0.gguf",
    ),
    "llama-2-13b-chat": ModelInfo(
        name="Llama-2-13b-chat",
        size=7.37,
        description="Meta developed and publicly released the Llama 2 family of large language models (LLMs), a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. Fine-tuned LLMs, called Llama-2-Chat, are optimized for dialogue use cases.",
        prompt_template=LLAMA_PROMPT_TEMPLATE,
        filename="llama-2-13b-chat.Q4_0.gguf",
        context_size=4096,
        url="https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q4_0.gguf",
    ),
    "llama-2-70b-chat": ModelInfo(
        name="Llama-2-70b-chat",
        size=38.9,
        description="Meta developed and publicly released the Llama 2 family of large language models (LLMs), a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. Fine-tuned LLMs, called Llama-2-Chat, are optimized for dialogue use cases.",
        prompt_template=LLAMA_PROMPT_TEMPLATE,
        filename="llama-2-70b-chat.Q4_0.gguf",
        context_size=4096,
        url="https://huggingface.co/TheBloke/Llama-2-70B-chat-GGUF/resolve/main/llama-2-70b-chat.Q4_0.gguf",
    ),
    "codellama-7b": ModelInfo(
        name="CodeLlama-7b",
        size=3.83,
        description="Code Llama is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 34 billion parameters. This model is designed for general code synthesis and understanding.",
        prompt_template=CODELLAMA_PROMPT_TEMPLATE,
        filename="codellama-7b.Q4_0.gguf",
        context_size=4096,
        url="https://huggingface.co/TheBloke/CodeLlama-7B-GGUF/resolve/main/codellama-7b.Q4_0.gguf",
    ),
    "codellama-13b": ModelInfo(
        name="CodeLlama-13b",
        size=7.37,
        description="Code Llama is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 34 billion parameters. This model is designed for general code synthesis and understanding.",
        prompt_template=CODELLAMA_PROMPT_TEMPLATE,
        filename="codellama-13b.Q4_0.gguf",
        context_size=4096,
        url="https://huggingface.co/TheBloke/CodeLlama-13B-GGUF/resolve/main/codellama-13b.Q4_0.gguf",
    ),
    "codellama-34b": ModelInfo(
        name="CodeLlama-34b",
        size=19.1,
        description="Code Llama is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 34 billion parameters. This model is designed for general code synthesis and understanding.",
        prompt_template=CODELLAMA_PROMPT_TEMPLATE,
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


def _print_model_not_found_message(model_name: str):
    print(f"[red]Model [code]{model_name}[/code] is not available.[/red]")
    names = [f"[code]{m}[/code]" for m in MODELS]
    available_models = ", ".join(names[:-1]) + " and " + names[-1]
    print(f"Available models: {available_models}")


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


def _try_llama_cpp_import() -> Any:
    # pylint: disable=import-error
    try:
        import llama_cpp

        return llama_cpp
    except:
        print(
            "Cannot run LLM; make sure you've installed the [code]llama-cpp-python[/code] package and dependencies!"
        )
        if _is_macos():
            print(
                'To install: [code]CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python[/code]'
            )
        else:
            print("To install: [code]pip install llama-cpp-python[/code]")
        print(
            "More information on how to install: [link]https://llama-cpp-python.readthedocs.io/en/latest/#installation[/link]"
        )
        print("Re-run this command after installation is done!")
        return None


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
        model = MODELS.get(model_name.lower())
        table = Table(show_header=False, box=None)
        table.add_column("Label", no_wrap=True, style="bold")
        table.add_column("Value")
        table.add_row("Model Name:", model.name)
        table.add_row("Size:", f"{model.size} GB")
        table.add_row("Description:", model.description)
        console.print(table)
    except:
        _print_model_not_found_message(model_name)


@oss_app.command("remove")
def model_remove(model_name: str):
    model = MODELS.get(model_name.lower())
    if not model:
        _print_model_not_found_message(model_name)
        return
    if _is_model_installed(model):
        _remove_model(model)
        print(f"LLM [bold]{model.name}[/bold] removed successfully.")
    else:
        print(f"[bold]{model.name}[/bold] not downloaded - nothing to remove.")


@oss_app.command("run")
def run_model(
    model_name: Optional[str] = typer.Argument("Llama-2-7b-chat"),
    host: Optional[str] = typer.Option(
        None, "--host", help="Hostname to run the LLM on."
    ),
    port: Optional[int] = typer.Option(None, "--port", help="Port to run the LLM on."),
):
    """Run a specific model."""
    llama_cpp = _try_llama_cpp_import()
    if not llama_cpp:
        return

    model = MODELS.get(model_name.lower())
    if not model:
        _print_model_not_found_message(model_name)
        return

    try:
        print(
            f"Preparing to download the {model_name} model from Huggingface. This might be a large file."
        )
        print(f"The model will be saved to: {MODEL_PATH}.")
        print(
            f"We appreciate your patience. If the download gets interrupted, don't worry, you can always resume it later."
        )
        _download_model(model.url, model.filename)
        print(f"Now loading {model.name}. Hang tight!")
    except KeyboardInterrupt:
        print("[red]Download interrupted.[/red]")
        print(
            f"You can resume it by running [code]opencopilot oss run {model_name}[/code] again."
        )
        return
    except:
        print(f"[red]Could not run {model_name}![/red]")
        return

    import uvicorn
    from opencopilot.oss_llm.app import create_app

    app = create_app(
        model=os.path.join(MODEL_PATH, model.filename),
        context_size=model.context_size,
    )
    uvicorn.run(
        app,
        host=host if host else "localhost",
        port=port if port else 8000,
    )


@oss_app.command("prompt")
def generate_prompt(model_name: str):
    """Generate a model-specific prompt template."""
    if model_name.lower() in MODELS:
        typer.echo(MODELS[model_name].prompt_template)
    else:
        _print_model_not_found_message(model_name)
