import re
import string
from typing import List
from uuid import UUID

import requests

from opencopilot.logger import api_logger
from opencopilot.repository.slack import slack_messenger

URL_REGEX = r"""((?:(?:https|ftp|http)?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|org|uk)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|uk|ac)\b/?(?!@)))"""

logger = api_logger.get()


def execute(text: str, conversation_id: UUID) -> None:
    urls: List[str] = _find_urls(text)
    for url in urls:
        _validate_url(url, conversation_id)


def _find_urls(text: str) -> List[str]:
    urls = re.findall(URL_REGEX, text)
    return ["".join(x for x in url if x in string.printable) for url in urls]


def _validate_url(url: str, conversation_id: UUID) -> None:
    try:
        response = requests.get(url)
        if response.status_code in [404, 410]:
            logger.warning(
                f"Error querying url {url}, conversation_id: {str(conversation_id)}"
            )
            slack_messenger.post_error(
                f"Error querying url {url}, conversation_id: {str(conversation_id)}",
                f"status_code {response.status_code}",
            )
    except Exception as e:
        logger.warning(
            f"Error querying url {url}, conversation_id: {str(conversation_id)}"
        )
        slack_messenger.post_error(
            f"Error querying url {url}, conversation_id: {str(conversation_id)}",
            str(e),
        )
