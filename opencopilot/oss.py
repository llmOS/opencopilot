import os
import typer
import psutil
import requests
from tqdm import tqdm
from rich import print
from rich.console import Console
from rich.table import Table
from dataclasses import dataclass

console = Console()

oss_app = typer.Typer(
    name="oss",
    help="OpenCopilot tool to manage and interact with Open Source LLMs.",
    no_args_is_help=True,
)

MODEL_PATH = ".models/"


@dataclass
class ModelInfo:
    name: str
    size: float
    description: str
    prompt_template: str
    filename: str
    url: str


MODELS = {
    "Llama-2-7b-chat": ModelInfo(
        name="llama-2-7b-chat",
        size=3.83,
        description="Meta developed and publicly released the Llama 2 family of large language models (LLMs), a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. Fine-tuned LLMs, called Llama-2-Chat, are optimized for dialogue use cases.",
        prompt_template="[INST] <<SYS>>\nYou are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n<</SYS>>\n{prompt}[/INST]",
        filename="llama-2-7b-chat.Q4_0.gguf",
        url="https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_0.gguf",
    ),
    "Llama-2-13b-chat": ModelInfo(
        name="Llama-2-13b-chat",
        size=7.37,
        description="Meta developed and publicly released the Llama 2 family of large language models (LLMs), a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. Fine-tuned LLMs, called Llama-2-Chat, are optimized for dialogue use cases.",
        prompt_template="[INST] <<SYS>>\nYou are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n<</SYS>>\n{prompt}[/INST]",
        filename="llama-2-13b-chat.Q4_0.gguf",
        url="https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q4_0.gguf",
    ),
    "Llama-2-70b-chat": ModelInfo(
        name="Llama-2-70b-chat",
        size=38.9,
        description="Meta developed and publicly released the Llama 2 family of large language models (LLMs), a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. Fine-tuned LLMs, called Llama-2-Chat, are optimized for dialogue use cases.",
        prompt_template="[INST] <<SYS>>\nYou are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n<</SYS>>\n{prompt}[/INST]",
        filename="llama-2-70b-chat.Q4_0.gguf",
        url="https://huggingface.co/TheBloke/Llama-2-70B-chat-GGUF/resolve/main/llama-2-70b-chat.Q4_0.gguf",
    ),
    "CodeLlama-7b": ModelInfo(
        name="CodeLlama-7b",
        size=3.83,
        description="Code Llama is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 34 billion parameters. This model is designed for general code synthesis and understanding.",
        prompt_template="None",
        filename="codellama-7b.Q4_0.gguf",
        url="https://huggingface.co/TheBloke/CodeLlama-7B-GGUF/resolve/main/codellama-7b.Q4_0.gguf",
    ),
    "CodeLlama-13b": ModelInfo(
        name="CodeLlama-13b",
        size=7.37,
        description="Code Llama is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 34 billion parameters. This model is designed for general code synthesis and understanding.",
        prompt_template="None",
        filename="codellama-13b.Q4_0.gguf",
        url="https://huggingface.co/TheBloke/CodeLlama-7B-GGUF/resolve/main/codellama-13b.Q4_0.gguf",
    ),
    "CodeLlama-34b": ModelInfo(
        name="CodeLlama-34b",
        size=19.1,
        description="Code Llama is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 34 billion parameters. This model is designed for general code synthesis and understanding.",
        prompt_template="None",
        filename="codellama-34b.Q4_0.gguf",
        url="https://huggingface.co/TheBloke/CodeLlama-34B-GGUF/resolve/main/codellama-34b.Q4_0.gguf",
    ),
}


def _can_use_model(model_size: float) -> bool:
    total_memory = psutil.virtual_memory().total / (1024**3)
    return model_size < total_memory / 2


def _is_model_installed(model_filename: str) -> bool:
    return os.path.exists(os.path.join(MODEL_PATH, model_filename))


def _download_model(url: str, filename: str) -> bool:
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

    os.makedirs(MODEL_PATH, exist_ok=True)
    with open(os.path.join(MODEL_PATH, filename), "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            progress_bar.update(len(chunk))
    progress_bar.close()


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
            "*" if _can_use_model(model.size) else "",
            model_name,
            f"{model.size}GB",
            "Yes" if _is_model_installed(model.filename) else "No",
        )
    console.print(table)
    print("\n* Recommended for your system")
    print("\nTo see more details about a model: [code]opencopilot oss info <model_name>[/code]")


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
        table.add_row("Requirements:", "16 GB RAM")
        console.print(table)
    except:
        typer.echo(f"Model {model_name} not found!")


@oss_app.command("run")
def run_model(model_name: str = "Llama-2-7b-chat"):
    """Run a specific model."""
    try:
        model = MODELS.get(model_name)
        if not _is_model_installed(model.filename):
            typer.echo(f"Downloading {model_name}...")
            _download_model(model.url, model.filename)
        typer.echo(f"Running {model.name}...")
    except:
        typer.echo(f"Could not run {model_name}!")
    try:
        import uvicorn
        from llama_cpp.server.app import create_app, Settings
    except:
        print("Coud not run llama-cpp, make sure you've installed [code]llama-cpp-python package![/code]"
        )
        print("Instructions how to install: [link]https://llama-cpp-python.readthedocs.io/en/latest/#installation[/link]")
        return
    settings = Settings(
        model=os.path.join(MODEL_PATH, model.filename),
        n_ctx=4096,
        n_gpu_layers=1,
        use_mlock=True,
    )
    app = create_app(settings=settings)
    uvicorn.run(
        app, host=os.getenv("HOST", "localhost"), port=int(os.getenv("PORT", 8000))
    )


@oss_app.command("prompt")
def generate_prompt(model_name: str):
    """Generate a model-specific prompt template."""
    if model_name in MODELS:
        typer.echo(MODELS[model_name].prompt_template)
    else:
        typer.echo(f"No prompt template available for {model_name}!")
