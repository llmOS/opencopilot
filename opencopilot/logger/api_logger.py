import logging
from typing import Optional
from uuid import UUID

from pythonjsonlogger import jsonlogger

LOGGING_MESSAGE_FORMAT = "%(asctime)s %(name)-12s %(levelname)s %(message)s"

logger: Optional[any] = None


def get(agent_id: UUID = None):
    global logger
    if logger:
        return logger
    console_handler = get_console_logger()
    logger = logging.getLogger("OpenCopilot")
    logger.setLevel(logging.DEBUG)

    logger.addHandler(console_handler)
    apply_default_formatter(console_handler)

    if agent_id:
        logger = logging.LoggerAdapter(logger, {"agent_id": str(agent_id)})
    return logger


def get_console_logger() -> logging.StreamHandler:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    return console_handler


def apply_default_formatter(handler: logging.Handler):
    formatter = jsonlogger.JsonFormatter(LOGGING_MESSAGE_FORMAT)
    handler.setFormatter(formatter)
