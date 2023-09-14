import uuid
import os
import enum
import xxhash
import platform
import subprocess
from subprocess import CalledProcessError
import importlib.metadata as importlib_metadata

import segment.analytics as segment_analytics


from . import settings
from .settings import Settings


SEGMENT_WRITE_KEY = "iEkciV19ocu9abTCzjbvjPsCKzOJF30S"
segment_analytics.write_key = SEGMENT_WRITE_KEY


class TrackingEventType(enum.Enum):
    COPILOT_START = 1
    CHAT_MESSAGE = 2


def get_opencopilot_version():
    package_name = "opencopilot-ai"
    declared_version = None

    try:
        declared_version = importlib_metadata.version(package_name)
    except importlib_metadata.PackageNotFoundError:
        pass  # Not installed

    # Run `pip freeze` to detect local install and get commit hash
    try:
        pip_freeze_output = subprocess.check_output(["pip", "freeze"]).decode("utf-8")
        matching_lines = [
            l for l in pip_freeze_output.split("\n") if "opencopilot" in l
        ]

        for line in matching_lines:
            if line.startswith(package_name):
                # Normal PyPI install
                declared_version = line.split("==")[1]
                break
            elif line.startswith(f"-e git+") and "egg=opencopilot_ai" in line:
                # Local install from version-controlled repo
                declared_version = line.split("-e ")[1]
                break
            elif "opencopilot-ai" in line or "opencopilot_ai" in line:
                # Local install from non-version-controlled directory
                declared_version = line
    except CalledProcessError:
        pass

    return declared_version

def is_running_in_replit():
    replit_conf_file_exists = os.path.isfile(".replit")
    return replit_conf_file_exists


def get_replit_owner_and_slug():
    repl_owner = os.environ.get("REPL_OWNER", "")
    repl_slug = os.environ.get("REPL_SLUG", "")
    return repl_owner, repl_slug

def get_repl_hash():
    """Returns a hashed unique identifier for the repl."""
    if is_running_in_replit():
        return hashed("/".join(get_replit_owner_and_slug()))
    return None

def hashed(s: str):
    return xxhash.xxh64(s.encode("utf-8")).hexdigest()


def get_hashed_user_id():
    """Returns a hashed unique identifier for the user."""
    if is_running_in_replit():
        # Replit has a unique user ID
        owner, _ = get_replit_owner_and_slug()
        return hashed(owner)

    # Fall back to mac address
    mac_address: int = uuid.getnode()
    return hashed(str(mac_address))


def track(event_type: TrackingEventType, *args, **kwargs):
    """Should be the entry point to all tracking."""
    tracking_enabled = settings.get().TRACKING_ENABLED

    if not tracking_enabled:
        return

    switcher = {
        TrackingEventType.COPILOT_START: _track_copilot_start,
        TrackingEventType.CHAT_MESSAGE: _track_chat_message,
    }

    func = switcher.get(event_type)
    if func is None:
        # We cannot raise an exception (to not break the app), and probably warning would be too much spam here too? So currently failing silently.
        # Alternatively, we could say in warning that your tracking is broken and just turn it off with OPENCOPILOT_DO_NOT_TRACK
        return

    try:
        func(*args, **kwargs)
    except Exception as e:
        # Same reason to hide exception as above
        pass


def _track_copilot_start(
    n_documents: int,
    n_data_loaders: int,
    n_local_files_dirs: int,
    n_local_file_paths: int,
    n_data_urls: int,
):
    """Should be fired when the copilot starts."""
    s: Settings = settings.get()

    repl_hash = get_repl_hash()
    llm_name = str(s.LLM)

    event = {
        "llm_name": llm_name,
        "copilot_name_hash": hashed(s.COPILOT_NAME),
        "repl_hash": repl_hash,
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


def _track_chat_message(user_agent, is_streaming):
    """Should be fired when a chat message is sent to the API."""
    copilot_name = settings.get().COPILOT_NAME
    event = {
        "is_streaming": is_streaming,
        "copilot_name_hash": hashed(copilot_name),
    }
    context = {
        "userAgent": user_agent,
    }

    segment_analytics.track(
        anonymous_id=get_hashed_user_id(),
        event="Messaged Copilot",
        properties=event,
        context=context,
    )
