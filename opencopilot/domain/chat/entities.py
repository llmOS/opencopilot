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
    chat_id: UUID
    content: str
    sources: List[str]


@dataclass(frozen=True)
class UserMessageInput:
    chat_id: UUID
    message: str
    response_message_id: str
    # TODO: rename to user_id
    email: str = None


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
    chat_id: UUID
    text: str
    sources: List[str]
    error: Optional[str] = None
    loading_message: Optional[LoadingMessage] = None

    def to_dict(self) -> Dict:
        result = {"text": self.text}
        if self.error:
            result["error"] = self.error
        if self.loading_message:
            result["loading_message"] = self.loading_message.to_dict()
        return result


@dataclass(frozen=True)
class ChatFeedbackInput:
    conversation_id: UUID
    correctness: int
    helpfulness: int
    easy_to_understand: int
    free_form_feedback: Optional[str] = None


@dataclass(frozen=True)
class ChatFeedbackOutput:
    response: str


@dataclass(frozen=True)
class ChatContextInput:
    conversation_id: UUID
    context: str


@dataclass(frozen=True)
class ChatContextOutput:
    response: str


@dataclass(frozen=True)
class ChatDeleteInput:
    conversation_id: UUID
    user_id: Optional[str] = None


@dataclass(frozen=True)
class ChatDeleteOutput:
    response: str
