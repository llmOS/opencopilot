from dataclasses import dataclass
from typing import List
from typing import Literal
from typing import Optional

from langchain import OpenAI

llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0)


@dataclass
class ExternalRoute:
    url: str
    description: str
    name: str
    type: Literal["copilot", "self"] = "copilot"


# Prompt taken from LlamaIndex (https://gpt-index.readthedocs.io/)
"""
descriptions format:
---------------------
(1) first description here

(1) second description here
---------------------
"""
ROUTE_DETECTION_PROMPT = f"""
Some choices are given below. It is provided in a numbered list (1 to {{count}}),where each item in the list corresponds to a summary.
---------------------
{{descriptions}}
---------------------
Using only the choices above and not prior knowledge, generate the selection object and reason that is most relevant to the question: '{{message}}'
"""


def execute(message: str, routes: List[ExternalRoute]) -> Optional[ExternalRoute]:
    try:
        llm_output = llm_call_intent(message, routes)
        result_parsed = ("".join([a for a in llm_output if a.isnumeric()]) or "0")[0]
        result_index = int(result_parsed) - 1
        if 0 <= result_index < len(routes):
            return routes[result_index]
    except:
        return None


def llm_call_intent(message: str, routes: List[ExternalRoute]) -> str:
    """
    Call the language model to classify the optimal routing.

    Args:
    message (str): The user's message for which intent is to be detected.

    Returns:
    str: The detected intent based on the model's prediction.
    """
    descriptions_formatted = ""
    for index, route in enumerate(routes):
        descriptions_formatted += f"({index + 1}) {route.description}"
        if index < (len(routes) - 1):
            descriptions_formatted += "\n\n"
    llm_output = llm(
        ROUTE_DETECTION_PROMPT.format(message=message, descriptions=descriptions_formatted, count=len(routes)))
    return llm_output


if __name__ == '__main__':
    test_cases = [
        "How can I improve my portfolio?",
        "How is my portfolio performing?",
        "How should I change my portfolio composition, if in any way?",
        "What is the level of risk I’m taking on with my current portfolio?",
        "What is the expected return of my portfolio in a 5-year and 10-year time horizon?",

        "Based on my goals and timelines, what stocks should I invest in?",
        "What are riskier investments right now that I should consider?",
        "What has happened in the financial markets today?",
        "How the stock price of Tesla changed historically and why?",
        "What were the financial results of Tesla in the last quarter?",
        "Is there a better company to pick as an investment in automotive industry than Tesla?",
        "Is Tesla under- or overvalued? Why?",
    ]

    possible_routes = [
        ExternalRoute(
            description="Useful for retrieving information related to user investments and portfolio", url="", name="Lightyear copilot"),
        ExternalRoute(
            description="Useful for retrieving information about the market and stocks in general", url="", name="Analyst copilot"),
    ]

    for t in test_cases:
        result = execute(t, possible_routes)
        print(result.name if result else None, t)
