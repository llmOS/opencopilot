from fastapi import APIRouter
from fastapi import Body
from opencopilot.logger import api_logger
from opencopilot.service.authorization import token_service
from opencopilot.service.authorization.entities import TokenRequest
from opencopilot.service.authorization.entities import TokenResponse

TAG = "Token"
router = APIRouter()
router.openapi_tags = [TAG]
router.title = "Authorization router"

logger = api_logger.get()


@router.post(
    "/tokens",
    tags=[TAG],
    summary="Generate a JSON Web Token.",
    response_model=TokenResponse,
)
async def evaluate(
    request: TokenRequest = Body(..., description="Token generation input")
):
    return token_service.execute(request)
