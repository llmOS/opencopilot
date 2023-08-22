<p align="center">
  <a href="https://docs.opencopilot.dev"><img src="https://github.com/opencopilotdev/opencopilot/assets/5147210/ff01df76-45f5-4c91-a4ef-cd9fcd73a971" alt="OpenCopilot"></a>
</p>
<p align="center">
    <em>OpenCopilot is a Python framework for building custom and private copilots.</em>
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

OpenCopilot is a Python framework for building custom and private copilots.

Building a Copilot that goes beyond a Twitter demo can be complex, time-consuming and unreliable. OpenCopilot makes building your own Copilot intuitive, fast and reliable: with it, you should be able to **build your copilot in a single day**.

### Key features

Here's what OpenCopilot comes with out of the box:

* Intuitive way to [define copilots in Python code](https://docs.opencopilot.dev//welcome/getting-started)
* Support for adding [knowledge bases](https://docs.opencopilot.dev//improve/knowledge-base) to your copilot ("chat with your data" style)
    * Use custom data sources, or any LangChain-compatible document loader
* [REST API](https://docs.opencopilot.dev//integrate/rest-api), including streaming support
* [Monitoring](https://docs.opencopilot.dev//integrate/monitoring) for your LLM & copilot usage
* [Front-end](https://github.com/opencopilotdev/opencopilot-frontend) template
* Use any LLM (`gpt-3.5-turbo-16k` by default)
* Coming soon: dynamic context, evaluation, and more


### Use cases

What can you do with copilots? Here are some examples:

1.  **Developer tooling Copilot**: [Ready Player Me](https://readyplayerdev.me/), the leading avatar tooling platform, built a CTO Copilot that helps their users integrate avatar SDK to games. In addition to providing code snippets, the copilot helps developers understand the product, integration errors, licensing concerns, third-party integrations, and much more. Click [here](https://rpm.opencopilot.dev/) to see copilot in action. Impact for Ready Player Me: **increased developer retention and happiness.**
2.  **SaaS Copilot**: [ChatSpot](https://chatspot.ai/), a Copilot by HubSpot enables their users to close deals faster, streamline RevOps and enable sales people to focus only on what matters by automating the tedious tasks. Most SaaS products are either overly complex and users don't get enough value of it. SaaS Copilots enable a human-like UX which drive their adoption.
3.  **E-commerce Copilot**: [Shopify](https://www.shopify.com/magic) Copilot is designed for store owners to grow revenue and simplify commerce. Essentially, a Copilot that enables to become a better entrepreneur on the Internet.
4.  **Company internal Copilot**: Companies spend enormous amount of money and time on building internal tools. Copilots can reduce that as it consolidates many SaaS products into one and can drive efficiency and cost savings across the company. For example, many startups pay hefty legal bills to their lawyers. At OpenCopilot we built an internal Legal Copilot which has reduced our legal spend by 50%. We've seen impactful Copilots built in the areas of HR, finance, operations, etc.
5.  **Individual/Creator Copilot**: ChatGPT is extremely powerful but held back because it's too generic and not personal enough. All of the founders at OpenCopilot have built a Founder Copilot which is personal and enables us with strategic decision making, executing at a high clip, etc. Also, creators can create their own Copilots which helps scale their time with their community.


## Quickstart

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
Your are a Parrot Copilot.
Your purpose is to repeat what the user says, but in a different wording.
You can use the context and history to do so.

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

That's it! The copilot is now running as an API service, at `localhost:3000` by default!

🎉 You can chat with it by calling the API:

```bash
curl -X 'POST' \
  'http://127.0.0.1:3000/v0/conversation/85ceff11-8072-47c8-a09a-ef846b024c04' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "inputs": "Hi! Who are you?"
}'
```

See the [interactive Swagger docs](http://localhost:3000/docs#/Chat/handle_conversation_v0_conversation__conversation_id__post) for full API documentation.

What next?

* **Start improving the copilot**: [customize your copilot](/improve/customize-your-copilot) by prompting, adding context, etc.
* Read more about the core features and stack choices of OpenCopilot in [Overview](/welcome/overview).


### Optional: front-end

As a pre-requisite, you need to have [`pnpm`](https://pnpm.io/) installed.

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

### Getting help

If you have any questions about OpenCopilot, feel free to do any of the following:

* Join our [Discord](https://discord.gg/AmdF5d94vE) and ask.
* Report bugs or feature requests in [GitHub issues](https://github.com/opencopilotdev/opencopilot/issues).
* Directly email Taivo, Co-founder & CTO of OpenCopilot: `taivo [at] opencopilot.dev`.
