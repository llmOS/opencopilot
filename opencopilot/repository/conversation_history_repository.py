import json
import os.path
from typing import Dict
from typing import List
from typing import Optional
from uuid import UUID

from opencopilot import settings
from opencopilot.logger import api_logger

DEFAULT_CONVERSATIONS_DIR = "logs/conversations"

logger = api_logger.get()


class ConversationHistoryRepositoryLocal:
    def __init__(
        self,
        conversations_dir: str = DEFAULT_CONVERSATIONS_DIR,
        question_key: str = "",
        response_key: str = "",
    ):
        self.conversations_dir = conversations_dir
        self.question_key = question_key or settings.get().PROMPT_QUESTION_KEY
        self.response_key = response_key or settings.get().PROMPT_ANSWER_KEY

    def get_prompt_history(self, conversation_id: UUID, count: Optional[int]) -> str:
        try:
            with open(self._get_file_path(conversation_id), "r") as f:
                history = json.load(f)
            if not count or len(history) <= count:
                return self._to_string(history)
            return self._to_string(history[count * -1 :])
        except:
            logger.debug(
                f"Cannot load conversation history, id: {str(conversation_id)}"
            )
        return ""

    def get_history(self, conversation_id: UUID) -> List[Dict]:
        history = []
        try:
            with open(self._get_file_path(conversation_id), "r") as f:
                history = json.load(f)
        except:
            pass
        return history

    def _to_string(self, history: List[Dict]) -> str:
        formatted: str = ""
        for i in history:
            formatted += f"{self.question_key}: {i.get('prompt', '')}\n"
            formatted += f"{self.response_key}: {i.get('response', '')}\n"
        return formatted

    def save_history(
        self,
        message: str,
        result: str,
        prompt_timestamp: float,
        response_timestamp: float,
        conversation_id: UUID,
        response_message_id: str,
    ) -> None:
        history = self.get_history(conversation_id)
        history.append(
            {
                "prompt": message,
                "response": result.strip(),
                "prompt_timestamp": prompt_timestamp,
                "response_timestamp": response_timestamp,
                "response_message_id": response_message_id,
            }
        )
        self._write_file(conversation_id, history)

    def remove_conversation(self, conversation_id: UUID) -> None:
        file_path = self._get_file_path(conversation_id)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

    def _get_file_path(self, conversation_id: UUID):
        return f"{self.conversations_dir}/{str(conversation_id)}.json"

    def _write_file(self, conversation_id: UUID, data):
        try:
            with open(self._get_file_path(conversation_id), "w") as f:
                f.write(json.dumps(data, indent=4))
        except Exception:
            logger.warning(f"Failed to save history for chat {str(conversation_id)}")
