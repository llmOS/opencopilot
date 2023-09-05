import hashlib
import platform
import pkg_resources

from . import settings
from .settings import Settings

from pprint import pprint

def is_tracking_enabled():
    s: Settings = settings.get()
    return s.TRACKING_ENABLED

def hashed(s: str):
    return hashlib.sha256(s.encode()).hexdigest()

def identify():
    pass # TODO

def track_copilot_start():
    if not is_tracking_enabled():
        return
    
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

def track_copilot_start_error():
    """Should be fired when the copilot fails to start."""
    if not is_tracking_enabled():
        return
    
    pass # TODO

def track_cli_command():
    """Should be fired when a CLI command is run."""
    if not is_tracking_enabled():
        return
    
    pass # TODO

def track_cli_error():
    """Should be fired when a CLI command fails."""
    if not is_tracking_enabled():
        return
    
    pass # TODO


def track_chat_message(user_agent, is_streaming):
    """Should be fired when a chat message is sent to the API."""
    if not is_tracking_enabled():
        return
    
    event = {
        "event_type": "chat_message",
        "user_agent": user_agent,
        "is_streaming": is_streaming
    }

    pprint(event)


def track_api_error():
    """Should be fired when an API error occurs."""
    if not is_tracking_enabled():
        return
    
    pass # TODO


#def track_error