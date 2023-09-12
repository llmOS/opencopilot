import json
import os
from typing import Dict
from typing import List
from uuid import UUID

from langchain.schema import Document

from opencopilot import settings
from opencopilot.logger import api_logger

logger = api_logger.get()


class ConversationLogsRepositoryLocal:
    def __init__(self, conversation_logs_dir: str = ""):
        if not conversation_logs_dir:
            conversation_logs_dir = os.path.join(
                settings.get().LOGS_DIR, "conversation_logs"
            )
        self.conversation_logs_dir = conversation_logs_dir

    def log_prompt_template(
        self,
        conversation_id: UUID,
        message: str,
        prompt_template: str,
        response_message_id: str,
        token_count: int = None,
    ) -> None:
        self._append_to_file(
            conversation_id,
            {
                "response_message_id": response_message_id,
                "message": message,
                "prompt_template": prompt_template,
                "token_count": token_count,
            },
        )

    def log_prompt_text(
        self,
        conversation_id: UUID,
        message: str,
        prompt_text: str,
        response_message_id: str,
        token_count: int = None,
    ) -> None:
        self._append_to_file(
            conversation_id,
            {
                "response_message_id": response_message_id,
                "message": message,
                "prompt_text": prompt_text,
                "token_count": token_count,
            },
        )

    def log_history(
        self,
        conversation_id: UUID,
        message: str,
        history: str,
        response_message_id: str,
        token_count: int = None,
    ) -> None:
        self._append_to_file(
            conversation_id,
            {
                "response_message_id": response_message_id,
                "message": message,
                "history": history,
                "token_count": token_count,
            },
        )

    def log_context(
        self,
        conversation_id: UUID,
        message: str,
        contexts: List[Document],
        response_message_id: str,
        token_count: int = None,
    ) -> None:
        self._append_to_file(
            conversation_id,
            {
                "response_message_id": response_message_id,
                "message": message,
                "context": json.dumps([c.dict() for c in contexts]),
                "token_count": token_count,
            },
        )

    def get_logs_by_message(
        self,
        conversation_id: UUID,
        response_message_id: str,
    ) -> List[Dict]:
        try:
            with open(self._get_file_path(conversation_id), "r") as file:
                lines = file.readlines()
            formatted_lines: List[Dict] = []
            for line in lines:
                if not isinstance(line, str):
                    continue
                formatted_line = json.loads(line)
                if formatted_line.get("response_message_id") == response_message_id:
                    formatted_lines.append(formatted_line)
            return formatted_lines
        except:
            return []

    def remove_conversation(self, conversation_id: UUID):
        file_path = self._get_file_path(conversation_id)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

    def _get_file_path(self, conversation_id: UUID):
        return os.path.join(self.conversation_logs_dir, str(conversation_id)) + ".jsonl"

    def _append_to_file(self, conversation_id: UUID, log: Dict) -> None:
        try:
            if not os.path.exists(self.conversation_logs_dir):
                os.makedirs(self.conversation_logs_dir, exist_ok=True)
            with open(self._get_file_path(conversation_id), "a") as file:
                file.write(json.dumps(log) + "\n")
        except:
            logger.error(
                f"Error log_prompt_text, conversation_id: {str(conversation_id)}"
            )
