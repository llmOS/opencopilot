import logging
from typing import Dict
from typing import Optional
from typing import Union

DEFAULT_LOG_LEVEL = logging.INFO
LOG_LEVELS: Dict[str, int] = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
}


def get():
    logging.basicConfig()
    logger = logging.getLogger("OpenCopilot")
    return logger


def set_log_level(log_level: Optional[Union[str, int]] = DEFAULT_LOG_LEVEL):
    logger = logging.getLogger("OpenCopilot")
    logger.setLevel(_convert_log_level(log_level))


def _convert_log_level(log_level: Optional[Union[str, int]]) -> int:
    if not log_level:
        log_level = DEFAULT_LOG_LEVEL
    elif isinstance(log_level, str):
        new_level = LOG_LEVELS.get(log_level)
        if new_level:
            log_level = new_level
        else:
            log_level = DEFAULT_LOG_LEVEL
    return log_level
