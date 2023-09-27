# OSS Copilot

Similar to the [llm_copilot](https://github.com/opencopilotdev/opencopilot/blob/main/examples/llm_copilot/README.md)  but leverages the open-source OSS LLama-2 model instead of proprietary OpenAI models.

## Install necessary packages
```
pip install -r requirements.txt
```
## Setup OSS LLM

Install `lama-cpp`, instructions [here](https://docs.opencopilot.dev/create/opensource-llms)

Start LLM:
```
opencopilot oss run llama-2-7b
```

## Start Copilot
```
python copilot.py
```
## Usage

Simply run and use `opencopilot chat` CLI to query the copilot.