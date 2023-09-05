import hashlib
import platform
import pkg_resources

from . import settings
from .settings import Settings

from pprint import pprint


def hashed(s: str):
    return hashlib.sha256(s.encode()).hexdigest()

def identify():
    pass # TODO

def track(event_name: str, *args, **kwargs):
    """Should be the entry point to all tracking."""
    tracking_enabled = settings.get().TRACKING_ENABLED

    if not tracking_enabled:
        return
    
    if event_name == "copilot_start":
        _track_copilot_start(*args, **kwargs)
    elif event_name == "copilot_start_error":
        _track_copilot_start_error(*args, **kwargs)
    elif event_name == "cli_command":
        _track_cli_command(*args, **kwargs)
    elif event_name == "cli_error":
        _track_cli_error(*args, **kwargs)
    elif event_name == "chat_message":
        _track_chat_message(*args, **kwargs)
    elif event_name == "api_error":
        _track_api_error(*args, **kwargs)
    else:
        raise Exception(f"Unknown tracking event name: {event_name}")


def _track_copilot_start():
    """Should be fired when the copilot starts."""
    s: Settings = settings.get()
    
    event = {
        "event_type": "copilot_start",
        "model_name": s.MODEL,
        "copilot_name_hash": hashed(s.COPILOT_NAME),
        "prompt": {
            "hash": hashed(s.PROMPT),
            "length": len(s.PROMPT)
        },
        "retriever": {
            # TODO name of retriever; num ingested docs & chunks
        },
        "features": {
            # TODO track how many URLs added, how many local data files/dirs, how many data loader functions
        },
        "system_information": {
            "python_version": platform.python_version(),
            "opencopilot_version": pkg_resources.get_distribution('opencopilot-ai').version,
            "platform.platform": platform.platform(),
            "platform.system": platform.system(),
            # TODO track env type - conda, venv, docker, etc
        }
    }

    pprint(event)

def _track_copilot_start_error():
    """Should be fired when the copilot fails to start."""
    pass # TODO

def _track_cli_command():
    """Should be fired when a CLI command is run."""
    pass # TODO

def _track_cli_error():
    """Should be fired when a CLI command fails."""
    pass # TODO


def _track_chat_message(user_agent, is_streaming):
    """Should be fired when a chat message is sent to the API."""
    event = {
        "event_type": "chat_message",
        "user_agent": user_agent,
        "is_streaming": is_streaming
    }

    pprint(event)


def _track_api_error():
    """Should be fired when an API error occurs."""
    pass # TODO
