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


## Overview

Copilots are becoming the new paradigm how to build successful LLM-based applications, as seen by Github , Shopify, Brex, Hubspot, etc Copilots. Yet, building a Copilot that goes beyond a Twitter demo is extremely complex as it's time-consuming, unreliable and feels like a massive undertaking. Moreover, existing solutions such as Microsoft Copilot Stack are closed-source. Building an LLM-app today feels like:

![Author: Soham Chatterjee](https://github.com/opencopilotdev/opencopilot/assets/3767980/f98def43-38b6-40ed-956b-8b5498c08318)

OpenCopilot solves this problem so building your own Copilot becomes intuitive, fast and reliable - all so **you can build your copilot in a single day**. For example, you can build Copilots such as:

**🛠️ Developer tooling Copilot**

* Example: [Stripe Copilot](https://stripe.com/newsroom/news/stripe-and-openai)
* End-to-end example: [Ready Player Me Copilot](https://github.com/opencopilotdev/opencopilot/tree/main/examples/ready_player_me_copilot) 

**💾 SaaS Copilot**

* Example: [HubSpot ChatSpot](https://chatspot.ai/)

**💳 E-commerce Copilot**

* Example: [Shopify Copilot](https://www.shopify.com/magic)
  
See more [use cases in docs](https://docs.opencopilot.dev/welcome/overview#use-cases).

## OpenCopilot overview

OpenCopilot provides one coherent end-to-end stack which is purposely designed for building a variety of copilots. From LLM selection (OSS LLMs upcoming), knowledge base, monitoring, evaluation, etc - it covers all the needs to build a useful copilot.

![opencopilot_stack](https://github.com/opencopilotdev/opencopilot/assets/5147210/140ca313-cf8a-4635-913e-8dbb5e33e8d4)

## Quickstart

As prerequisites, you need to have **Python 3.8+** and **pip** installed.

### 1. Install the Python package

```bash
pip install opencopilot-ai
```

### 2. Create a minimal Copilot

Into a Python file (for example, `copilot.py`), add:


```python
from opencopilot import OpenCopilot

copilot = OpenCopilot(
    openai_api_key="your-openai-api-key",
    llm_model_name="gpt-4",
    prompt_file="my_prompt.txt"
    )

# Run the copilot
copilot()
```

Make sure your custom prompt file exists: in `my_prompt.txt`, add the following:

```txt
Your are a Parrot Copilot. Your purpose is to repeat what the user says, but in a different wording.

=========
{context}
=========

{history}
User: {question}
Parrot Copilot answer in Markdown:
```

The template variables will be filled at runtime; see our docs on [Prompting](https://docs.opencopilot.dev/improve/prompting) if you'd like to learn more.

### 3. Run the Copilot

```bash
python copilot.py
```

That's it! Your minimal copilot is now running as an API service, at `localhost:3000` by default 🎉

You can quickly test and chat with it in the terminal by running:

```bash
opencopilot chat "Hello, who are you?"
```

See the [interactive Swagger docs](http://localhost:3000/docs#/Chat/handle_conversation_v0_conversation__conversation_id__post) for full API documentation.

## 📖 Customizing, improving, testing and deploying your Copilot

Please see the full [documentation](https://docs.opencopilot.dev/welcome/introduction) to:

* **Start improving your copilot**: [customize your copilot by prompting](https://docs.opencopilot.dev/improve/customize-your-copilot), adding knowledge base, etc.
* Read more about the core features and stack choices of OpenCopilot in [Overview](/welcome/overview).

## Optional: front-end

If you'd like to have a front-end for your Copilot, then you can easily deploy it. As a pre-requisite, you need to have [`pnpm`](https://pnpm.io/) installed.

First, clone the [opencopilotdev/opencopilot-frontend](https://github.com/opencopilotdev/opencopilot-frontend) repository:

```bash
git clone https://github.com/opencopilotdev/opencopilot-frontend
```

Then, setup the environment variables:

```bash
cd opencopilot-frontend
cp .env.example .env
```

Install the dependencies:

```bash
pnpm install
```

Run the front-end application:

```bash
pnpm run dev
```

You can now access the front-end at http://localhost:3001.

## Getting help

If you have any questions about OpenCopilot, feel free to do any of the following:

* Join our [Discord](https://discord.gg/AmdF5d94vE) and ask.
* Report bugs or feature requests in [GitHub issues](https://github.com/opencopilotdev/opencopilot/issues).
* Directly email Taivo, Co-founder & CTO of OpenCopilot: `taivo@opencopilot.dev`.
