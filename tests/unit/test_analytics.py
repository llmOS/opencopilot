from unittest.mock import patch
from unittest.mock import MagicMock
import opencopilot.settings as settings
from opencopilot.analytics import track
from opencopilot.analytics import TrackingEventType

import opencopilot.analytics as analytics



def test_tracking_disabled():
    settings._settings = MagicMock()
    settings._settings.TRACKING_ENABLED = False

    with patch("opencopilot.analytics._track_copilot_start") as mock:
        track(TrackingEventType.COPILOT_START)

    assert not mock.called


def test_tracking_enabled():
    settings._settings = MagicMock()
    settings._settings.TRACKING_ENABLED = True

    with patch("opencopilot.analytics._track_copilot_start") as mock:
        track(TrackingEventType.COPILOT_START)

    assert mock.called
    

def test_tracking_enabled_env(monkeypatch):
    settings._settings = None
    monkeypatch.delenv("OPENCOPILOT_DO_NOT_TRACK", raising=False)

    with patch("opencopilot.analytics._track_copilot_error") as mock:
        track(TrackingEventType.COPILOT_ERROR)

    assert mock.called


def test_tracking_disabled_env(monkeypatch):
    settings._settings = None
    monkeypatch.setenv("OPENCOPILOT_DO_NOT_TRACK", "true")

    with patch("opencopilot.analytics._track_copilot_error") as mock:
        track(TrackingEventType.COPILOT_ERROR)

    assert not mock.called

def test_get_opencopilot_version_pypi_install():
    analytics.subprocess = MagicMock()
    analytics.subprocess.check_output.return_value = "\n".join([
        "openai==0.27.8",
        "opencopilot-ai==0.3.4"
    ]).encode("utf-8")

    assert analytics.get_opencopilot_version() == "0.3.4"


def test_get_opencopilot_version_local_install():
    analytics.subprocess = MagicMock()
    analytics.subprocess.check_output.return_value = "\n".join([
        "openai==0.27.8",
        "-e git+ssh://git@github.com/opencopilotdev/opencopilot.git@ec45b0d7ae639ab4e23217319649c82ffbafbf2c#egg=opencopilot_ai",
        "pathspec==0.11.2"
    ]).encode("utf-8")

    assert analytics.get_opencopilot_version() == "git+ssh://git@github.com/opencopilotdev/opencopilot.git@ec45b0d7ae639ab4e23217319649c82ffbafbf2c#egg=opencopilot_ai"


def test_get_opencopilot_version_local_dir():
    analytics.subprocess = MagicMock()
    analytics.subprocess.check_output.return_value = "\n".join(["openapi-schema-pydantic==1.2.4",
        "# Editable install with no version control (opencopilot-ai==0.3.4)",
        "-e /Users/taivo/opencopilot/local_ocp",
        "openpyxl==3.1.2"]).encode("utf-8")


    assert analytics.get_opencopilot_version() == "# Editable install with no version control (opencopilot-ai==0.3.4)"


