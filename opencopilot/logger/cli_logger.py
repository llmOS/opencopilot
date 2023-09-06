import logging
from typing import Optional

logger: Optional[any] = None


def get():
    global logger
    if logger:
        return logger
    logger = logging.getLogger("OpenCopilot")
    logger.setLevel(logging.DEBUG)
    return logger
