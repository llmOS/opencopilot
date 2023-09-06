import sys

from opencopilot.domain.errors import CopilotConfigurationError
from opencopilot.domain.errors import CopilotRuntimeError

DEV_MODE_ENABLED = False


def add_copilot_exception_catching(logger):
    def on_crash(exctype, value, traceback):
        # "exctype" is the class of the exception raised
        # "value" is the instance
        # "traceback" is the object containing what python needs to print
        if not DEV_MODE_ENABLED:
            if issubclass(exctype, CopilotConfigurationError):
                # Instead of the stack trace, we print an error message to stderr
                logger.error(f"{exctype.__name__}: {value}")
            elif issubclass(exctype, CopilotRuntimeError):
                logger.error(f"{exctype.__name__}: {value}")
            else:
                # sys.__excepthook__ is the default excepthook that prints the stack trace
                # so we use it directly if we want to see it
                sys.__excepthook__(exctype, value, traceback)
        else:
            sys.__excepthook__(exctype, value, traceback)

    # Now we replace the default excepthook by our own
    sys.excepthook = on_crash
