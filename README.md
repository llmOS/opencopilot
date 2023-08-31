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

Copilots are becoming the new paradigm how to build successful LLM-based applications, as seen by [Github](https://github.com/features/copilot), [Shopify](https://www.shopify.com/magic), [Brex](https://www.brex.com/journal/press/brex-openai-ai-tools-for-finance-teams), [Hubspot](https://app.hubspot.com/chatspot/chat), etc Copilots. Yet, building a Copilot that goes beyond a Twitter demo is extremely complex as it's time-consuming, unreliable and feels like a massive undertaking. Moreover, existing solutions such as Microsoft Copilot Stack are closed-source. Building an LLM-app today feels like:

![Author: Soham Chatterjee](https://github.com/opencopilotdev/opencopilot/assets/3767980/f98def43-38b6-40ed-956b-8b5498c08318)

OpenCopilot solves this problem so building your own Copilot becomes intuitive, fast and reliable - all so **you can build your copilot in a single day**. For example, you can build Copilots such as:

**🛠️ Developer tooling Copilot**

* End-to-end example: [Ready Player Me Copilot](https://github.com/opencopilotdev/opencopilot/tree/main/examples/ready_player_me_copilot)
* Example: [Stripe Copilot](https://stripe.com/newsroom/news/stripe-and-openai)

**💾 SaaS Copilot**

* Example: [HubSpot ChatSpot](https://chatspot.ai/)

**💳 E-commerce Copilot**

* Example: [Shopify Copilot](https://www.shopify.com/magic)
  
See more [use cases in docs](https://docs.opencopilot.dev/welcome/overview#use-cases).



## 🔍 Stack Overview
OpenCopilot provides one coherent end-to-end stack which is purposely designed for building a variety of copilots. From LLM selection (OSS LLMs upcoming), knowledge base, monitoring, evaluation, etc - it covers all the needs to build a useful copilot.

![opencopilot_stack](https://github.com/opencopilotdev/opencopilot/assets/5147210/140ca313-cf8a-4635-913e-8dbb5e33e8d4)

See our docs on [Stack Overview](https://docs.opencopilot.dev/welcome/overview#stack-overview) to learn more about each part of the OpenCopilot stack.

## ⚡ Quickstart

As prerequisites, you need to have **Python 3.8+** and **pip** installed.

### 1. Install the OpenCopilot Python package

```bash
pip install opencopilot-ai
```

### 2. Create a new python file to set up a minimal Copilot
For example, `copilot.py`, where you add the code from below. Also, add your own `openai_api_key`, which you can get [from here](https://platform.openai.com/account/api-keys).

If you have access to GPT-4, change `llm_model_name` to `gpt-4`.

```python
from opencopilot import OpenCopilot

PROMPT = """
You are a Parrot Copilot. Your purpose is to repeat what the user says, but in a different wording.

=========
{context}
=========

{history}
User: {question}
Parrot Copilot answer in Markdown:
"""

copilot = OpenCopilot(
    openai_api_key="your-openai-api-key",
    llm_model_name="gpt-3.5-turbo-16k",
    prompt=PROMPT
    )

# Run the copilot
copilot()
```

In the prompt, the template variables will be filled at runtime; see our docs on [Prompting](https://docs.opencopilot.dev/improve/prompting) if you'd like to learn more.

See our docs on [Configuration](https://docs.opencopilot.dev/integrate/configuration) if you'd like to learn more about other configuration options.

### 3. Run the Copilot

```bash
python copilot.py
```

Your minimal copilot is now running as an API service, at `localhost:3000` by default. To see the full API documentation, go to [interactive Swagger docs](http://localhost:3000/docs#/Chat/handle_conversation_v0_conversation__conversation_id__post).

### 4. Chat with the Copilot
You can quickly test out and chat with your copilot using the command-line interface by running:

```bash
opencopilot chat "Hello, who are you?"
```

## 📖 Customizing, improving, testing and deploying your Copilot

While setting up the minimal copilot is quick, easy and fun, adding knowledge base to your copilot unlocks a whole new experience. Read how to customize your Copilot from the [documentation](https://docs.opencopilot.dev/improve/customize-your-copilot), which covers:

* Customizing your copilot with prompting
* Adding knowledge base
* Automatic evaluation
* Debugging LLM generation, retrieval, etc.
* Read more about the core features and stack choices of OpenCopilot in [Overview](https://docs.opencopilot.dev/welcome/overview).

## Optional: front-end

If you'd like to set up an out of the box front-end for your Copilot, follow the instructions in the [opencopilotdev/opencopilot-frontend](https://github.com/opencopilotdev/opencopilot-frontend) repository.

<img width="666" alt="Screenshot 2023-08-28 at 14 23 39" src="https://github.com/opencopilotdev/opencopilot/assets/22053381/6eab1f6a-a3ad-4649-a5e9-9abeb2ffcee9">



## Getting help

If you have any questions about OpenCopilot, feel free to do any of the following:

* Join our [Discord](https://discord.gg/AmdF5d94vE) and ask.
* Report bugs or feature requests in [GitHub issues](https://github.com/opencopilotdev/opencopilot/issues).
* Directly email Taivo, Co-founder & CTO of OpenCopilot: `taivo@opencopilot.dev`.
