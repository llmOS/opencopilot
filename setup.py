import os
import platform

from setuptools import setup


def package_files(directory):
    paths = []
    for path, directories, filenames in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


def set_env():
    if platform.system() == "Darwin":
        os.system('export CMAKE_ARGS="-DLLAMA_METAL=on"')


set_env()
extra_files = package_files("opencopilot")

setup(
    name='opencopilot-ai',
    version='0.3.7',
    packages=["opencopilot"],
    package_data={"": extra_files},
    license="MIT",
    description="OpenCopilot Backend",
    author="OpenCopilot",
    author_email="kaspar@nftport.xyz",
    url="https://github.com/opencopilotdev/opencopilot",
    py_modules=["opencopilot"],
    install_requires=[
        "fastapi",
        "dataclasses-json",
        "python-dotenv",
        "python-json-logger",
        "uvicorn",
        "pandas",
        "pexpect",
        "langchain>=0.0.217",
        "passlib",
        "pyjwt[crypto]",
        "Jinja2",
        "tiktoken",
        "weaviate-client>=3.23.2",
        "pypdf",
        "unstructured",
        "pdf2image",
        "openai",
        "unstructured",
        "xxhash",
        "omegaconf",
        "openpyxl",
        "typer[all]",
        "trafilatura",
        "filetype",
        "segment-analytics-python",
        "psutil",
    ],
    extras_require={
        "llama": [
            "llama-cpp-python==0.1.83",
        ],
    },
    entry_points={
        "console_scripts": [
            "opencopilot = opencopilot.cli:app",
        ],
    },
)
