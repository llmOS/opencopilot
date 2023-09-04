import hashlib
import platform
import pkg_resources

from . import settings
from .settings import Settings

from pprint import pprint


def hashed(s: str):
    return hashlib.sha256(s.encode()).hexdigest()

def track_copilot_start():
    
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