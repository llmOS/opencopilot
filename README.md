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
It's designed to be **fast to get started, extensible, and easy to use**.
Using OpenCopilot, you can see your copilot come live in 5 minutes, and
making a fully functional copilot should take you **less than a day**.


Example Copilots built with OpenCopilot

- [Ready Player Me Copilot](https://rpm.opencopilot.dev/) which helps developers integrate RPM avatar SDK into their games.
- [Unity Copilot](https://unity.opencopilot.dev/) which helps Unity developers debug, write code and speed up their development flow.

## Quickstart

### 1. Install the Python package

```bash
pip install opencopilot-ai
```

### 2. Create a minimal Copilot

Into a Python file (for example, `copilot.py`), add:


```python
from opencopilot import OpenCopilot

copilot = OpenCopilot()
copilot()
```

### 3. Run the Copilot

```bash
python copilot.py
```

That's it! The copilot is now running as an API service! 🎉 You can now chat with it: TODO how? (CLI, frontend, etc)

OpenCopilot by default helps you setup a Python API service for your copilot. That is intentional: we expect most people to integrate the functionality into their own application. However, if you want to setup a front-end for your copilot, we provide a working NextJS application out of the box. Follow the steps below to do so.


### Front-end

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

### What next?

* Make the copilot yours: [customize your copilot](https://docs.opencopilot.dev/improve/customize-your-copilot) by prompting, adding context, etc.
* Read more about the core features and stack choices of OpenCopilot in [Overview](https://docs.opencopilot.dev/welcome/overview).

### Getting help

If you have any questions about OpenCopilot, feel free to do any of the following:

* Join our [Discord](https://discord.gg/AmdF5d94vE) and ask in the **#support** channel.
* Report bugs or feature requests in [GitHub issues](https://github.com/opencopilotdev/opencopilot/issues).
* Directly email Taivo, Co-founder & CTO of OpenCopilot: `taivo [at] opencopilot.dev`.
