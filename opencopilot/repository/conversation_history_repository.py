import json
import os.path
from typing import Dict
from typing import List
from typing import Union
from typing import Optional
from uuid import UUID
from langchain.schema import HumanMessage
from langchain.schema import AIMessage

from opencopilot import settings
from opencopilot.logger import api_logger

logger = api_logger.get()


class ConversationHistoryRepositoryLocal:
    """
    Manages the storage and retrieval of conversation histories locally.

    This repository provides mechanisms to save, fetch, and format conversations for prompts,
    and is backed by the local file system. Conversation histories include both human
    and AI messages, and additional metadata like timestamps.
    """

    def __init__(
        self,
        conversations_dir: str = "",
        question_template: str = "",
        response_template: str = "",
    ):
        """
        Initialize the repository with directory and message templates.

        Args:
            conversations_dir (str, optional): Directory to store conversation histories. Uses default if not provided.
            question_template (str, optional): Template to format human messages. Uses default if not provided.
            response_template (str, optional): Template to format AI responses. Uses default if not provided.
        """
        if not conversations_dir:
            conversations_dir = os.path.join(settings.get().LOGS_DIR, "conversations")
        self.conversations_dir = conversations_dir
        self.question_template = question_template or settings.get().QUESTION_TEMPLATE
        self.response_template = response_template or settings.get().RESPONSE_TEMPLATE

    def get_history_for_prompt(
        self, conversation_id: UUID, count: Optional[int]
    ) -> str:
        """
        Get the prompt-formatted history for a given conversation id.

        Args:
            conversation_id (UUID): The unique identifier for the conversation.
            count (Optional[int]): Number of conversation prompts to fetch. If not provided, fetches all.

        Returns:
            str: Conversation history formatted for inclusion into the prompt.
        """
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
        """
        Fetch the conversation history for a given conversation id.

        Args:
            conversation_id (UUID): The unique identifier for the conversation.

        Returns:
            List[Dict]: Conversation history as list of dictionaries with "prompt"/"response" message pair plus additional data.
        """
        history = []
        try:
            with open(self._get_file_path(conversation_id), "r") as f:
                history = json.load(f)
        except:
            pass
        return history

    def get_messages(
        self, conversation_id: UUID
    ) -> List[Union[HumanMessage, AIMessage]]:
        """
        Fetch the conversation history for a given conversation id as Langchain messages.

        Args:
            conversation_id (UUID): The unique identifier for the conversation.

        Returns:
            List[Union[HumanMessage, AIMessage]]: Conversation history in LangChain HumanMessage/AIMessage format.
        """
        history = self.get_history(conversation_id)
        messages = []
        for message_pair in history:
            messages.append(HumanMessage(content=message_pair["prompt"]))
            messages.append(AIMessage(content=message_pair["response"]))
        return messages

    def _to_string(self, history: List[Dict]) -> str:
        """
        Convert a conversation history list to a formatted string.

        The conversation history list consists of dictionaries with "prompt" and "response" pairs.
        This method uses the provided question and response templates to format them.

        Args:
            history (List[Dict]): The list of message pairs to be formatted.

        Returns:
            str: Formatted conversation history as a string.
        """
        formatted: str = ""
        for i in history:
            formatted += (
                f"{self.question_template.format(question=i.get('prompt', ''))}\n"
            )
            formatted += (
                f"{self.response_template.format(response=i.get('response', ''))}\n"
            )
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
        """
        Save a user message and AIs response to the history.

        Args:
            message (str): The original message/prompt.
            result (str): The AI's response to the message.
            prompt_timestamp (float): Timestamp of when the prompt was sent.
            response_timestamp (float): Timestamp of when the response was received.
            conversation_id (UUID): The unique identifier for the conversation.
            response_message_id (str): ID of the response message.

        Returns:
            None
        """
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
        """
        Remove a conversation's history given its id.

        Args:
            conversation_id (UUID): The unique identifier for the conversation.

        Returns:
            None
        """
        file_path = self._get_file_path(conversation_id)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

    def _get_file_path(self, conversation_id: UUID):
        """
        Get the file path for a given conversation ID.

        Args:
            conversation_id (UUID): The unique identifier for the conversation.

        Returns:
            str: File path for the conversation's data.
        """
        return f"{self.conversations_dir}/{str(conversation_id)}.json"

    def _write_file(self, conversation_id: UUID, data):
        """
        Write the conversation data to the corresponding file.

        Args:
            conversation_id (UUID): The unique identifier for the conversation.
            data: The data to be saved.

        Returns:
            None
        """
        try:
            if not os.path.exists(self.conversations_dir):
                os.makedirs(self.conversations_dir, exist_ok=True)
            with open(self._get_file_path(conversation_id), "w") as f:
                f.write(json.dumps(data, indent=4))
        except Exception:
            logger.warning(f"Failed to save history for chat {str(conversation_id)}")
