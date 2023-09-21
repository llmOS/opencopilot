from typing import Optional

import pydantic
from pydantic import BaseModel
from pydantic import Field

from opencopilot.service.entities import ApiResponse


class ValueWithTokens(BaseModel):
    value: str = Field()
    token_count: Optional[int] = Field(
        description="If debug mode is enabled will include token counts."
    )


class GetMessageDebugResponse(ApiResponse):
    prompt_template: Optional[ValueWithTokens] = Field(
        description="Prompt template used."
    )
    data_sources: Optional[str] = Field(
        description="List of data sources used in string json format."
    )
    user_question: Optional[ValueWithTokens] = Field(description="User question.")
    # citations: List[str] = Field(
    #     description="List of citations used in the final prompt."
    # )
    context: Optional[ValueWithTokens] = Field(
        description="List of context strings used the final prompt in json format."
    )
    chat_history: Optional[ValueWithTokens] = Field(
        description="Chat history used in the final prompt in json format."
    )
    full_prompt: Optional[ValueWithTokens] = Field(
        description="Final prompt used in the LLM call."
    )
    llm_response: Optional[ValueWithTokens] = Field(description="LLM answer.")

    if pydantic.__version__.startswith("2"):
        model_config = {
            "json_schema_extra": {
                "example": {
                    "response": "OK",
                    "prompt_template": "You are a copilot.\n{context} {history} {answer}",
                    # TODO:
                    "data_sources": ["{}"],
                    "user_question": "Who are you?",
                    # "citations": "Who are you?",
                    "context": [
                        '[{"page_content": "This is some text from the data files.", "metadata": {"source": "copilots/data/test.txt"}}]'
                    ],
                    "chat_history": [
                        '[{"user": "Who are you?", {"copilot": "I am a copilot."}]'
                    ],
                    "full_prompt": "Full formatted prompt text here",
                    "llm_response": "I am a copilot.",
                }
            }
        }


class EvaluationInput(BaseModel):
    query: str = Field(description="Query sent to the conversation endpoint.")
    answer: str = Field(description="Answer from the conversation endpoint.")
    expected_answer: str = Field(description="Expected answer.")


class EvaluationResponse(ApiResponse):
    evaluation: str = Field(
        description="Evaluation result, a grade from A-F, with A being the best grade."
    )

    if pydantic.__version__.startswith("2"):
        model_config = {
            "json_schema_extra": {
                "example": {
                    "response": "OK",
                    "evaluation": "B",
                }
            }
        }
