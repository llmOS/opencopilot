from fastapi import APIRouter
from fastapi import Body
from fastapi import Path

from opencopilot.logger import api_logger
from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)
from opencopilot.repository.conversation_logs_repository import (
    ConversationLogsRepositoryLocal,
)
from opencopilot.service.debug import message_debug_service
from opencopilot.service.debug.entities import EvaluationInput
from opencopilot.service.debug.entities import EvaluationResponse
from opencopilot.service.debug.entities import GetMessageDebugResponse
from opencopilot.service.evaluate import evaluation_service

TAG = "Conversation"
router = APIRouter()
router.openapi_tags = [TAG]
router.title = "Debug router"

logger = api_logger.get()


@router.get(
    "/debug/{conversation_id}/{message_id}",
    tags=[TAG],
    summary="Get debug information about a message.",
    response_model=GetMessageDebugResponse,
)
async def get_copilots(
    conversation_id: str = Path(..., description="The ID of the conversation."),
    message_id: str = Path(..., description="The ID of the response message."),
):
    history_repository = ConversationHistoryRepositoryLocal()
    logs_repository = ConversationLogsRepositoryLocal()

    return message_debug_service.execute(
        conversation_id,
        message_id,
        history_repository,
        logs_repository,
    )
