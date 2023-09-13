from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class ChatConversationsInput:
    user_id: Optional[str] = None


@dataclass(frozen=True)
class ChatConversationsOutput:
    conversations: List[str]


@dataclass(frozen=True)
class MessageModel:
    conversation_id: UUID
    content: str
    sources: List[str]


@dataclass(frozen=True)
class UserMessageInput:
    conversation_id: UUID
    message: str
    response_message_id: str
    user_id: str = None


@dataclass(frozen=True)
class LoadingMessage:
    message: str
    called_copilot: Optional[str]

    def to_dict(self) -> Dict:
        result = {"message": self.message}
        if self.called_copilot:
            result["called_copilot"] = self.called_copilot
        return result

    @staticmethod
    def from_dict(loading_message: Dict):
        return LoadingMessage(
            message=loading_message.get("message") or "",
            called_copilot=loading_message.get("called_copilot") or None,
        )


@dataclass(frozen=True)
class StreamingChunk:
    conversation_id: UUID
    text: str
    sources: List[str]
    error: Optional[str] = None
    loading_message: Optional[LoadingMessage] = None
    response_message_id: Optional[str] = None

    def to_dict(self) -> Dict:
        result = {"text": self.text}
        if self.error:
            result["error"] = self.error
        if self.loading_message:
            result["loading_message"] = self.loading_message.to_dict()
        if self.response_message_id:
            result["response_message_id"] = self.response_message_id
        return result


@dataclass(frozen=True)
class ChatDeleteInput:
    conversation_id: UUID
    user_id: Optional[str] = None


@dataclass(frozen=True)
class ChatDeleteOutput:
    response: str
