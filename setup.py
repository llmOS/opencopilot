import os

from setuptools import setup


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('opencopilot')

setup(
    name='opencopilot-ai',
    version='0.3.3',
    packages=["opencopilot"],
    package_data={'': extra_files},
    license="MIT",
    description="OpenCopilot Backend",
    author="OpenCopilot",
    author_email="kaspar@nftport.xyz",
    url="https://github.com/opencopilotdev/opencopilot",
    py_modules=['opencopilot'],
    install_requires=[
        'fastapi',
        'dataclasses-json',
        'python-dotenv',
        'python-json-logger',
        'uvicorn',
        'pandas',
        'pexpect',
        'langchain>=0.0.217',
        'passlib',
        'pyjwt[crypto]',
        'Jinja2',
        'tiktoken',
        'text-generation',
        'weaviate-client',
        'pypdf',
        'unstructured',
        'pdf2image',
        'openai',
        'unstructured',
        'xxhash',
        'omegaconf',
        'openpyxl',
        'typer[all]',
    ],
    entry_points={
        'console_scripts': [
            'opencopilot = opencopilot.cli:app',
        ],
    },
)
