import logging


def get():
    logging.basicConfig()
    logger = logging.getLogger("OpenCopilot")
    return logger
