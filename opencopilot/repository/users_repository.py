import json
import os
from typing import Dict
from typing import List
from typing import Optional
from uuid import UUID

import xxhash

from opencopilot import settings
from opencopilot.logger import api_logger

DEFAULT_USER_NAME = "default_user"

logger = api_logger.get()


class UsersRepositoryLocal:
    def __init__(self, users_dir: str = ""):
        if not users_dir:
            users_dir = os.path.join(settings.get().LOGS_DIR, "users")
        os.makedirs(users_dir, exist_ok=True)
        self.users_dir = users_dir

    def get_conversations(self, user_id: Optional[str] = None) -> List[str]:
        data = self._read_file(user_id)
        if data:
            return data.get("conversations") or []
        return []

    def add_conversation(
        self, conversation_id: UUID, user_id: Optional[str] = None
    ) -> None:
        data = self._read_file(user_id)
        if data.get("conversations"):
            conversations = set(data.get("conversations"))
            conversations.add(str(conversation_id))
            data["conversations"] = sorted(list(conversations))
        else:
            data["conversations"] = [str(conversation_id)]
        self._write_file(data, user_id)

    def remove_conversation(
        self, conversation_id: UUID, user_id: Optional[str] = None
    ) -> None:
        data = self._read_file(user_id)
        if data.get("conversations"):
            conversations = set(data.get("conversations"))
            if str(conversation_id) in conversations:
                conversations.remove(str(conversation_id))
                data["conversations"] = sorted(list(conversations))
                self._write_file(data, user_id)

    def _read_file(self, user_id: Optional[str] = None) -> Dict:
        try:
            file_path = self._get_file_path(user_id)
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def _write_file(self, data: Dict, user_id: Optional[str] = None):
        file_path = self._get_file_path(user_id)
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=4))

    def _get_file_path(self, user_id: Optional[str] = None) -> str:
        if not user_id:
            user_id = DEFAULT_USER_NAME
        file_name = xxhash.xxh64(user_id.encode("utf-8")).hexdigest()
        return os.path.join(self.users_dir, file_name) + ".json"
