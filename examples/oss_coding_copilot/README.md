# OSS coding copilot

A specialized copilot that crafts code to address coding challenges, ensuring that solutions meet constraints and pass provided test cases. This uses the CodeLlama engine. Detailed 

## Install necessary packages
```
pip install -r requirements.txt
```
## Setup OSS LLM

Install `lama-cpp`, instructions [here](https://docs.opencopilot.dev/create/opensource-llms)

Start LLM:
```
opencopilot oss run codellama-7b
```

## Start Copilot
```
python copilot.py
```
## Usage

Simply run and use `opencopilot chat` CLI to query the copilot.
