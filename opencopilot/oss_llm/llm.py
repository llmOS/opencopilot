from llama_cpp import Llama
from typing import List
import json


class LLamaLLM:
    def __init__(self, model: str, context_size: int) -> None:
        self.context_size = context_size
        self.model = Llama(
            model_path=model, use_mlock=True, n_ctx=context_size, n_gpu_layers=-1
        )

    def generate(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int,
        stop: List[str] = ["###", "User:", "[INST]"],
    ) -> str:
        for token in self.model(
            prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            stop=stop,
        ):
            output = {"token": {"text": token["choices"][0]["text"]}}
            output = "data:" + json.dumps(output) + "\n"
            output = output.encode("utf-8")
            yield output

    def tokenize(self, text: str) -> List[int]:
        return self.model.tokenize(text.encode("utf-8"))
