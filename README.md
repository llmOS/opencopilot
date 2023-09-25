<p align="center">
  <a href="https://docs.opencopilot.dev"><img src="https://github.com/opencopilotdev/opencopilot/assets/5147210/ff01df76-45f5-4c91-a4ef-cd9fcd73a971" alt="OpenCopilot"></a>
</p>
<p align="center">
    <em> 🕊️ OpenCopilot: Build and embed open-source AI Copilots into your product with ease</em>
</p>
<p align="center">

<a href="https://github.com/opencopilotdev/opencopilot/actions/workflows/unit_test.yml" target="_blank">
    <img src="https://github.com/opencopilotdev/opencopilot/actions/workflows/unit_test.yml/badge.svg" alt="Unit tests">
</a>

<a href="https://github.com/opencopilotdev/opencopilot/actions/workflows/e2e_test_full.yml" target="_blank">
    <img src="https://github.com/opencopilotdev/opencopilot/actions/workflows/e2e_test_full.yml/badge.svg" alt="E2E tests">
</a>

<a href="https://twitter.com/OpenCopilot" target="_blank">
    <img src="https://img.shields.io/twitter/url/https/twitter.com/opencopilot.svg?style=social&label=Follow%20%40OpenCopilot" alt="Package version">
</a>

<a href="https://discord.gg/AmdF5d94vE" target="_blank">
    <img src="https://img.shields.io/discord/1133675019478782072?logo=discord&label=OpenCopilot" alt="Package version">
</a>

<a href="https://pypi.org/project/opencopilot-ai" target="_blank">
    <img src="https://img.shields.io/pypi/v/opencopilot-ai?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

<p align="center">
  <b>Documentation:</b> <a href="https://docs.opencopilot.dev/">docs.opencopilot.dev</a>
</p>


## 🕊️ OpenCopilot Overview

Copilots are becoming the new paradigm how to build successful LLM-based applications, as seen by [Github](https://github.com/features/copilot), [Shopify](https://www.shopify.com/magic), [Brex](https://www.brex.com/journal/press/brex-openai-ai-tools-for-finance-teams), [Hubspot](https://app.hubspot.com/chatspot/chat), etc Copilots. Yet, building a Copilot that goes beyond a Twitter demo is time-consuming, unreliable and overly complex. Moreover, existing solutions such as Microsoft Copilot Stack are closed-source. Today, building an LLM-app feels like:

![Author: Soham Chatterjee](https://github.com/opencopilotdev/opencopilot/assets/3767980/f98def43-38b6-40ed-956b-8b5498c08318)

OpenCopilot solves this problem so building your own Copilot becomes intuitive, fast and reliable - all so **you can build your copilot in a single day**. For example, you can build Copilots such as:

**🛠️ Developer tooling Copilot**

* Example: [Ready Player Me Copilot](https://venturebeat.com/games/ready-player-me-launches-ai-based-copilot-to-help-developers-streamline-avatars/)
* Implementation: [Code](https://github.com/opencopilotdev/opencopilot/tree/main/examples/ready_player_me_copilot)

**💾 SaaS Copilot**

* Example: [HubSpot ChatSpot](https://chatspot.ai/)

**💳 E-commerce Copilot**

* Example: [Shopify Copilot](https://www.shopify.com/magic)
  
See more [use cases in docs](https://docs.opencopilot.dev/welcome/use-cases).


## ⚡ Quickstart

As prerequisites, you need to have **Python 3.8+** and **pip** installed.

### 1. Install the OpenCopilot Python package

```bash
pip install opencopilot-ai
```

### 2. Create a new python file to set up a minimal Copilot

For example, you can create an AWS CLI Copilot using the following code by adding it to a `copilot.py` file. **Make sure to replace** `openai_api_key` with your 🔑 [own OpenAI API key](https://platform.openai.com/account/api-keys).

```python
from opencopilot import OpenCopilot

PROMPT = """
You are an Amazon Web Services (AWS) CLI copilot. You are an interactive version of AWS CLI documentation and chat with developers who need help using it.
Your mission is to be a reliable companion throughout the developer journey - always ready to answer questions and share insights.

=========
{context}
=========

{history}
User: {question}
AWS CLI Copilot answer in Markdown:
"""

copilot = OpenCopilot(
    copilot_name="AWS CLI Copilot",
    openai_api_key="your-openai-api-key",
    # You can also use gpt-4 for improved accuracy
    # or Llama 2 locally (https://docs.opencopilot.dev/create/opensource-llms#running-an-llm)
    llm="gpt-3.5-turbo-16k",
    prompt=PROMPT,
)

# Download and embed the knowledge base from given URL
copilot.add_data_urls(
    [
        "https://awsdocs.s3.amazonaws.com/cli/latest/aws-cli.pdf",
    ]
)

# Run the copilot
copilot()
```

### 3. Run the Copilot

```bash
python copilot.py
```

### 4. Chat with the Copilot
You can chat with your copilot in the UI at [localhost:3000/ui](http://localhost:3000/ui) or using the CLI:

```bash
opencopilot chat "Hello, who are you?"
```

### 5. Create your own copilot

After seeing how easy it is to set up a copilot, you can now create your own and level it up step by step. For this, see [docs.opencopilot.dev](https://docs.opencopilot.dev/create/iterative-development), or check a more detailed example of the AWS copilot in the [examples directory](examples/aws_copilot/).

## Available Examples

OpenCopilot provides a collection of sample projects to demonstrate its various functionalities. Here's a brief overview of each:

- **aws_copilot**: Amazon Web Services (AWS) CLI copilot. An interactive version of AWS CLI documentation that interacts with developers in need of assistance. Its task is to accompany developers throughout their journey, offering valuable insights and answers.

- **coding_copilot**: A copilot that writes code to solve coding problems. It ensures the code adheres to constraints and passes the test cases. Utilizes CodeLlama for its operations.

- **custom_prompt_builder**: Demonstrates the usage of the `prompt_builder` decorator. It intelligently builds custom prompts based on user intent. The function identifies the intent behind a user's message and crafts a specific prompt in response.

- **docker_deployment**: A hands-on example showing how to deploy a project utilizing OpenCopilot inside a docker container.

- **llm_copilot**: A Large Language Model (LLM) Copilot that acts as an interactive guide for OpenCopilot developer documentation. It aids developers seeking help with OpenCopilot, pointing them to the right sections and providing valuable insights.

- **oss_copilot**: A variant of the llm_copilot but uses the open-source OSS LLama-2 model instead of the proprietary OpenAI models.

- **ready_player_me_copilot**: Acts as a copilot for Ready Player Me (RPM) developer documentation. It's designed to assist developers building on top of RPM, guiding them through their journey and offering assistance as needed.

For a deep dive into each example, visit the [examples directory](https://github.com/opencopilotdev/opencopilot/tree/main/examples).

## 🔍 Stack Overview
OpenCopilot provides one coherent end-to-end stack which is purposely designed for building a variety of copilots. From LLM selection (OSS LLMs upcoming), knowledge base, monitoring, evaluation, etc - it covers all the needs to build a useful copilot.

![opencopilot_stack](https://github.com/opencopilotdev/opencopilot/assets/5147210/140ca313-cf8a-4635-913e-8dbb5e33e8d4)

See our docs on [Stack Overview](https://docs.opencopilot.dev/welcome/overview) to learn more about each part of the OpenCopilot stack.

## Analytics

OpenCopilot collects library usage data to improve the product and your experience. We collect events regarding errors and your usage of copilot features, and never collect your code, prompts, knowledge base documents, or LLM outputs. To understand what is tracked, check out the [tracking code](/opencopilot/analytics.py).

You can opt out of tracking by setting the environment variable `OPENCOPILOT_DO_NOT_TRACK=True`:

```bash
export OPENCOPILOT_DO_NOT_TRACK=True
```

## Example copilots


## Getting help

If you have any questions about OpenCopilot, feel free to do any of the following:

* Join our [Discord](https://discord.gg/AmdF5d94vE) and ask.
* Report bugs or feature requests in [GitHub issues](https://github.com/opencopilotdev/opencopilot/issues).
* Directly email Taivo, Co-founder & CTO of OpenCopilot: `taivo@opencopilot.dev`.