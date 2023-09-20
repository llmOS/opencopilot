import enum
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import SystemMessage

chat = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0, max_tokens=5)

class Intent(enum.Enum):
    """Enumeration for classifying user intent."""
    GREETING = enum.auto()
    THANKS = enum.auto()
    OTHER = enum.auto()

INTENT_DETECTION_PROMPT = f"""
You are an Intent Detection Copilot, your mission is to accurately detect and understand the user's intent from a given set of options. You have the ability to analyze user input and classify it into three categories: {", ".join(e.name for e in Intent)} Your goal is to assist developers in creating conversational agents that can appropriately respond to user interactions based on their intent. You excel at natural language processing and machine learning techniques to effectively identify and classify user intents. Your superpower is understanding the nuances of user language and providing precise intent detection for seamless user experiences.

The user message is: {{message}}
Detected intent category:
"""

def llm_call_intent(message: str):
    """
    Call the language model to classify the intent of a given message.

    Args:
    message (str): The user's message for which intent is to be detected.

    Returns:
    str: The detected intent based on the model's prediction.
    """
    llm_input = [SystemMessage(content=INTENT_DETECTION_PROMPT.format(message=message))]
    llm_output = chat(llm_input, max_tokens=5, stop=["\n"])
    return llm_output.content

def detect_intent(message: str):
    """
    Detect user intent based on the message.

    Args:
    message (str): The user's message for which intent is to be detected.

    Returns:
    Intent: An enum member representing the detected intent (GREETING, THANKS, OTHER).
    """
    llm_output = llm_call_intent(message)
    intent = Intent[llm_output.strip()]
    return intent
