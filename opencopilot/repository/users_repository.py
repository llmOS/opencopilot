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
    """
    A local repository for managing users and their associated conversations.

    This class provides a way to persistently store and manage user-related data,
    such as the conversations associated with each user. It leverages a local file
    storage mechanism, with each user's data being stored as a separate JSON file.
    The file names are hashes of user IDs, providing a consistent and obfuscated
    naming convention.

    By default, if no user ID is provided in any of the methods, a default user is
    assumed. This class also provides methods to add or remove conversations for a
    specific user, as well as to fetch a list of all conversations associated with a user.

    Attributes:
        users_dir (str): The directory where user data files are stored.

    Note:
        This class is intended to be used in environments where a local storage
        solution for user data is appropriate. For larger or distributed systems,
        a more robust database solution might be more suitable.
    """

    def __init__(self, users_dir: str = ""):
        """
        Initialize the local users repository.

        Args:
            users_dir (str): Path to the directory where user data is stored.
                            If not provided, defaults to the LOGS_DIR setting.
        """
        if not users_dir:
            users_dir = os.path.join(settings.get().LOGS_DIR, "users")
        os.makedirs(users_dir, exist_ok=True)
        self.users_dir = users_dir

    def get_conversations(self, user_id: Optional[str] = None) -> List[str]:
        """
        Retrieve the list of conversation IDs associated with a user.

        Args:
            user_id (Optional[str]): The identifier for the user. If not provided, the default user is used.

        Returns:
            List[str]: A list of conversation IDs.
        """
        data = self._read_file(user_id)
        if data:
            return data.get("conversations") or []
        return []

    def add_conversation(
        self, conversation_id: UUID, user_id: Optional[str] = None
    ) -> None:
        """
        Add a conversation ID to the list of conversations associated with a user.

        Args:
            conversation_id (UUID): The unique identifier for the conversation to be added.
            user_id (Optional[str]): The identifier for the user. If not provided, the default user is used.

        Returns:
            None
        """
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
        """
        Remove a conversation ID from the list of conversations associated with a user.

        Args:
            conversation_id (UUID): The unique identifier for the conversation to be removed.
            user_id (Optional[str]): The identifier for the user. If not provided, the default user is used.

        Returns:
            None
        """
        data = self._read_file(user_id)
        if data.get("conversations"):
            conversations = set(data.get("conversations"))
            if str(conversation_id) in conversations:
                conversations.remove(str(conversation_id))
                data["conversations"] = sorted(list(conversations))
                self._write_file(data, user_id)

    def _read_file(self, user_id: Optional[str] = None) -> Dict:
        """
        Read user data from the file.

        Args:
            user_id (Optional[str]): The identifier for the user. If not provided, the default user is used.

        Returns:
            Dict: The user data, or an empty dictionary if the file doesn't exist.
        """
        try:
            file_path = self._get_file_path(user_id)
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def _write_file(self, data: Dict, user_id: Optional[str] = None):
        """
        Write user data to the file.

        Args:
            data (Dict): The user data to be written.
            user_id (Optional[str]): The identifier for the user. If not provided, the default user is used.

        Returns:
            None
        """
        file_path = self._get_file_path(user_id)
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=4))

    def _get_file_path(self, user_id: Optional[str] = None) -> str:
        """
        Compute the file path for the given user ID.

        The method hashes the user ID to get the filename, which is stored in the specified directory.

        Args:
            user_id (Optional[str]): The identifier for the user. If not provided, the default user is used.

        Returns:
            str: Path to the file for the user.
        """
        if not user_id:
            user_id = DEFAULT_USER_NAME
        file_name = xxhash.xxh64(user_id.encode("utf-8")).hexdigest()
        return os.path.join(self.users_dir, file_name) + ".json"
