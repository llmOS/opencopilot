from dataclasses import dataclass


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
        size=3.83,
        description="Code Llama is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 34 billion parameters. This model is designed for general code synthesis and understanding.",
        prompt_template="None",
        filename="codellama-13b.Q4_0.gguf",
        url="https://huggingface.co/TheBloke/CodeLlama-7B-GGUF/resolve/main/codellama-13b.Q4_0.gguf",
    ),
    "CodeLlama-34b": ModelInfo(
        name="CodeLlama-34b",
        size=3.83,
        description="Code Llama is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 34 billion parameters. This model is designed for general code synthesis and understanding.",
        prompt_template="None",
        filename="codellama-34b.Q4_0.gguf",
        url="https://huggingface.co/TheBloke/CodeLlama-34B-GGUF/resolve/main/codellama-34b.Q4_0.gguf",
    ),
}
