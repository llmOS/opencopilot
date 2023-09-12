from threading import Lock

from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from opencopilot.oss_llm.entities import GenerateStreamRequest
from opencopilot.oss_llm.entities import TokenizeRequest
from opencopilot.oss_llm.entities import TokenizeResponse
from opencopilot.oss_llm.llm import LLamaLLM

router = APIRouter()

llama_lock = Lock()


def _get_llama():
    try:
        llama_lock.acquire()
        yield llm
    except:
        return None
    finally:
        llama_lock.release()


def create_app(model: str, context_size: int) -> FastAPI:
    global llm
    llm = LLamaLLM(model=model, context_size=context_size)
    app = FastAPI(
        title="Local LLM API",
        version="0.0.1",
    )
    app.include_router(router)
    return app


@router.get("/")
async def index():
    return {"title": "OSS LLM API"}


@router.post("/generate_stream")
async def generate_stream(
    request: GenerateStreamRequest, llama: LLamaLLM = Depends(_get_llama)
):
    return StreamingResponse(
        llama.generate(request.query, request.temperature, request.max_tokens),
        media_type="text/event-stream",
    )


@router.post("/tokenize", response_model=TokenizeResponse)
async def tokenize(request: TokenizeRequest, llama: LLamaLLM = Depends(_get_llama)):
    return TokenizeResponse(tokens=llama.tokenize(request.text))
