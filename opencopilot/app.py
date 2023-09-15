import asyncio
import os
import webbrowser

from fastapi import FastAPI
from fastapi import Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

import opencopilot
from opencopilot import settings
from opencopilot.logger import api_logger
from opencopilot.routers import main_router
from opencopilot.routers import routing_utils
from opencopilot.service.exception_handlers.exception_handlers import (
    custom_exception_handler,
)
from opencopilot.service.middleware.main_middleware import MainMiddleware
from opencopilot.service.middleware.request_enrichment_middleware import (
    RequestEnrichmentMiddleware,
)

app = FastAPI()

app.include_router(main_router.router, prefix="/v0")

html_template_path = os.path.join(os.path.dirname(opencopilot.__file__), "html")
templates = Jinja2Templates(directory=html_template_path)

API_TITLE = "OpenCopilot API"
API_DESCRIPTION = (
    "OpenCopilot API, for more information visit https://docs.opencopilot.dev/"
)
API_VERSION = "0.1"

app.copilot_callbacks = None

base_url = settings.get().get_base_url()

logger = api_logger.get()


@app.on_event("startup")
async def startup_event():
    # TODO: once we support multiple workers move this to application.py
    loop = asyncio.get_event_loop()
    loop.create_task(_open_browser())


async def _open_browser():
    await asyncio.sleep(1)
    logger.info(f"Started chat UI on {base_url}/ui")
    try:
        cache_dir: str = os.path.expanduser("~/.opencopilot")
        if os.path.exists(cache_dir):
            return
        webbrowser.open(f"{base_url}/ui", new=2)
        os.makedirs(cache_dir, exist_ok=True)
    except:
        pass


class ApiInfo(BaseModel):
    title: str
    description: str
    version: str

    class Config:
        schema_extra = {
            "example": {
                "title": API_TITLE,
                "description": API_DESCRIPTION,
                "version": API_VERSION,
            }
        }


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
        routes=app.routes,
        servers=_get_servers(),
    )
    openapi_schema["info"]["contact"] = {"name": "", "email": ""}
    openapi_schema["info"]["x-logo"] = {"url": ""}
    openapi_schema["x-readme"] = {
        "samples-languages": ["curl", "node", "javascript", "python"]
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def _get_servers():
    servers = []
    if settings.get().is_production():
        pass
    else:
        servers.append({"url": f"{base_url}"})
    return servers


app.openapi = custom_openapi

# order of middleware matters! first middleware called is the last one added
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get().ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(MainMiddleware)
app.add_middleware(RequestEnrichmentMiddleware)

# exception handlers run AFTER the middlewares!
# Handles API error responses
app.add_exception_handler(Exception, custom_exception_handler)


# Overrides FastAPI error responses, eg: authorization, not found
# app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
# Overrides default Pydantic request validation errors
# app.add_exception_handler(RequestValidationError, validation_exception_handler)


def get_api_info() -> ApiInfo:
    return ApiInfo(title=API_TITLE, description=API_DESCRIPTION, version=API_VERSION)


@app.get(
    "/",
    summary="Returns API information",
    description="Returns API information",
    response_description="API information with title, description and version.",
    response_model=ApiInfo,
    include_in_schema=not settings.get().is_production(),
)
def root():
    return routing_utils.to_json_response(get_api_info().dict())


@app.get("/ui", include_in_schema=False, response_class=HTMLResponse)
def ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
