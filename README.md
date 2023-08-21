# OpenCopilot 🕊️


![Discord](https://img.shields.io/discord/1133675019478782072?logo=discord&label=OpenCopilot)

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, high performance, easy to learn, fast to code, ready for production</em>
</p>
<p align="center">

<a href="https://github.com/opencopilotdev/opencopilot/actions/workflows/unit_test.yml" target="_blank">
    <img src="https://github.com/opencopilotdev/opencopilot/actions/workflows/unit_test.yml/badge.svg" alt="Unit tests">
</a>

<a href="https://github.com/opencopilotdev/opencopilot/actions/workflows/e2e_test_linux_native_openai.yml" target="_blank">
    <img src="https://github.com/opencopilotdev/opencopilot/actions/workflows/e2e_test_linux_native_openai.yml/badge.svg" alt="E2E Test Linux Native">
</a>

<a href="https://twitter.com/OpenCopilot" target="_blank">
    <img src="https://img.shields.io/twitter/url/https/twitter.com/opencopilot.svg?style=social&label=Follow%20%40OpenCopilot" alt="Package version">
</a>

<a href="https://twitter.com/OpenCopilot" target="_blank">
    <img src="https://img.shields.io/discord/1133675019478782072?logo=discord&label=OpenCopilot" alt="Package version">
</a>

<a href="https://pypi.org/project/opencopilot-ai" target="_blank">
    <img src="https://img.shields.io/pypi/v/opencopilot-ai?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

**Documentation**: [docs.opencopilot.dev](https://docs.opencopilot.dev/)


## Overview

OpenCopilot is a Python framework for building custom and private copilots.
It's designed to be **fast to get started, extensible, and easy to use**.
Using OpenCopilot, you can see your copilot come live in 5 minutes, and
making a fully functional copilot should take you **less than a day**.


**Example Copilots built with OpenCopilot**

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

First, clone the repo you're in: [opencopilotdev/opencopilot](https://github.com/opencopilotdev/opencopilot):

```bash
git clone git@github.com:opencopilotdev/opencopilot.git
```

Then, setup the environment variables:

```bash
cd opencopilot/frontend
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
