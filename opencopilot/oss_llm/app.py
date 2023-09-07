from fastapi import FastAPI, APIRouter
from fastapi.responses import StreamingResponse
from opencopilot.oss_llm.entities import GenerateStreamRequest
from opencopilot.oss_llm.entities import TokenizeRequest
from opencopilot.oss_llm.entities import TokenizeResponse
from opencopilot.oss_llm.llm import LLamaLLM

router = APIRouter()


def create_app(model: str, context_size: int) -> FastAPI:
    global llm
    llm = LLamaLLM(model=model, context_size=context_size)
    app = FastAPI(
        title="Local LLM API",
        version="0.0.1",
    )
    app.include_router(router)
    return app


@router.post("/generate_stream")
async def generate_stream(request: GenerateStreamRequest):
    return StreamingResponse(
        llm.generate(request.query, request.temperature, request.max_tokens),
        media_type="text/event-stream",
    )


@router.post("/tokenize", response_model=TokenizeResponse)
async def tokenize(request: TokenizeRequest):
    return TokenizeResponse(tokens=llm.tokenize(request.text))
