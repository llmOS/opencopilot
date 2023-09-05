import uuid
import xxhash
import platform
import importlib_metadata

import segment.analytics as segment_analytics


from . import settings
from .settings import Settings


SEGMENT_WRITE_KEY = "wZRhqA6Rt6sDtro2TayQM6mw7vuxXOtR"
segment_analytics.write_key = SEGMENT_WRITE_KEY
segment_analytics.debug = True
# segment_analytics.send = False


def get_opencopilot_version():
    package_name = "opencopilot-ai"
    declared_version = importlib_metadata.version(package_name)

    # TODO currently will not show correctly if installed locally with `pip install -e .`
    return declared_version


def hashed(s: str):
    return xxhash.xxh64(s.encode("utf-8")).hexdigest()


def get_hashed_user_id():
    """Returns a hashed unique identifier for the user."""
    mac_address: int = uuid.getnode()
    return hashed(str(mac_address))


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


def _track_copilot_start(
    n_documents: int,
    n_data_loaders: int,
    n_local_files_dirs: int,
    n_local_file_paths: int,
    n_data_urls: int,
):
    """Should be fired when the copilot starts."""
    s: Settings = settings.get()

    event = {
        "llm_name": s.MODEL,
        "copilot_name_hash": hashed(s.COPILOT_NAME),
        "prompt": {"hash": hashed(s.PROMPT), "length": len(s.PROMPT)},
        "retrieval": {
            "n_documents": n_documents,
            "n_data_loaders": n_data_loaders,
            "n_local_files_dirs": n_local_files_dirs,
            "n_data_urls": n_data_urls,
            "n_local_file_paths": n_local_file_paths,
        },
        "environment": {
            "python_version": platform.python_version(),
            "opencopilot_version": get_opencopilot_version(),
            "platform.platform": platform.platform(),
            "platform.system": platform.system(),
            # TODO track env type - conda, venv, docker, etc
        },
    }

    segment_analytics.track(
        anonymous_id=get_hashed_user_id(), event="Started Copilot", properties=event
    )


def _track_copilot_start_error():
    """Should be fired when the copilot fails to start."""
    # TODO add this when CLI error handling is implemented in a separate
    pass


def _track_cli_command(subcommand: str):
    """Should be fired when a CLI command is run."""
    event = {
        "subcommand": subcommand,
    }

    segment_analytics.track(
        anonymous_id=get_hashed_user_id(), event="Used CLI", properties=event
    )


def _track_cli_error():
    """Should be fired when a CLI command fails."""
    # TODO add this when error handling is implemented in a separate PR
    # TODO - should we actually add this as a field under _track_cli_command?
    pass


def _track_chat_message(user_agent, is_streaming):
    """Should be fired when a chat message is sent to the API."""
    event = {
        "user_agent": user_agent,
        "is_streaming": is_streaming,
    }

    segment_analytics.track(
        anonymous_id=get_hashed_user_id(), event="Messaged Copilot", properties=event
    )


def _track_api_error():
    """Should be fired when an API error occurs."""
    # TODO add this when error handling is implemented in a separate
    pass
