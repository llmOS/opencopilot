from typing import List

from opencopilot.domain.chat.entities import UserMessageHistoryItem
from opencopilot.service.chat.entities import MessageHistoryItem


def convert_message_history(
    history: List[MessageHistoryItem],
) -> List[UserMessageHistoryItem]:
    result = []
    if history:
        for item in history:
            result.append(UserMessageHistoryItem(type=item.type, message=item.message))
    return result
