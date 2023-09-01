from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path

from opencopilot.authorization import validate_api_key_use_case
from opencopilot.logger import api_logger
from opencopilot.repository.conversation_history_repository import (
    ConversationHistoryRepositoryLocal,
)
from opencopilot.repository.conversation_logs_repository import (
    ConversationLogsRepositoryLocal,
)
from opencopilot.repository.users_repository import UsersRepositoryLocal
from opencopilot.service.debug import message_debug_service
from opencopilot.service.debug.entities import GetMessageDebugResponse

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
    user_id: str = Depends(validate_api_key_use_case.execute),
):
    history_repository = ConversationHistoryRepositoryLocal()
    logs_repository = ConversationLogsRepositoryLocal()
    users_repository = UsersRepositoryLocal()

    return message_debug_service.execute(
        conversation_id,
        message_id,
        history_repository,
        logs_repository,
        users_repository=users_repository,
        user_id=user_id,
    )
