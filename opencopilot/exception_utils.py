import logging
import sys

from colorama import Fore
from colorama import Style

from opencopilot.domain.errors import CopilotConfigurationError
from opencopilot.domain.errors import CopilotRuntimeError
from opencopilot.logger import api_logger


def add_copilot_exception_catching():
    def on_crash(exctype, value, traceback):
        # "exctype" is the class of the exception raised
        # "value" is the instance
        # "traceback" is the object containing what python needs to print
        # logger = logging.getLogger("OpenCopilot")
        logger = api_logger.get()
        if logger.level >= logging.INFO:
            if issubclass(exctype, CopilotConfigurationError) or issubclass(
                exctype, CopilotRuntimeError
            ):
                # Instead of the stack trace, we print an error message to stderr
                logger.error(f"{Fore.RED}{exctype.__name__}{Style.RESET_ALL}: {value}")
            else:
                # sys.__excepthook__ is the default excepthook that prints the stack trace
                # so we use it directly if we want to see it
                sys.__excepthook__(exctype, value, traceback)
        else:
            sys.__excepthook__(exctype, value, traceback)

    # Now we replace the default excepthook by our own
    sys.excepthook = on_crash
