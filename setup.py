from setuptools import setup

setup(
    name='opencopilot-ai',
    version='0.1.0',
    packages=["opencopilot"],
    license="MIT",
    description="OpenCopilot Backend",
    author="OpenCopilot",
    author_email="kaspar@nftport.xyz",
    url="https://github.com/opencopilotdev/opencopilot",
    py_modules=['opencopilot'],
    install_requires=[
        'fastapi==0.95.1',
        'psycopg2-binary==2.9.6',
        'python-dotenv==1.0.0',
        'python-json-logger==2.0.7',
        'sqlalchemy==2.0.1',
        'uvicorn==0.21.1',
        'pandas==1.5.3',
        'pexpect==4.8.0',
        'gunicorn==20.1.0',
        'langchain==0.0.236',
        'passlib==1.7.4',
        'pyjwt[crypto]===2.6.0',
        'Jinja2==3.1.2',
        'tiktoken==0.4.0',
        'text-generation==0.6.0',
        'weaviate-client==3.19.2',
        'pytest==7.3.1',
        'pytest-cov==4.1.0',
        'pytest-asyncio==0.21.0',
        'pypdf==3.9.1',
        'unstructured==0.7.2',
        'pdf2image==1.16.3',
        'sentence_transformers==2.2.2',
        'matplotlib==3.7.1',
        'beautifulsoup4==4.12.2',
        'openai==0.27.8',
        'wandb==0.15.4',
        'streamlit==1.24.0',
        'playwright==1.35.0',
        'unstructured==0.7.2',
        'dataclasses-json==0.5.9',
        'omegaconf==2.3.0',
        'GitPython==3.1.31',
        'pytesseract==0.3.10',
        'aiohttp==3.8.5',
        'xxhash==3.3.0',
    ],
)
