from langchain.chat_models import ChatOpenAI


class LocalLLM(ChatOpenAI):
    openai_api_key: str = "LOCAL_LLM"
    llm_url: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, openai_api_base=kwargs["llm_url"])
