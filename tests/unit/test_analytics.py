from unittest.mock import patch
from unittest.mock import MagicMock
import opencopilot.settings as settings
from opencopilot.analytics import track



def test_tracking_disabled():
    settings._settings = MagicMock()
    settings._settings.TRACKING_ENABLED = False

    with patch("opencopilot.analytics._track_copilot_start") as mock:
        track("copilot_start")

    assert not mock.called


def test_tracking_enabled():
    settings._settings = MagicMock()
    settings._settings.TRACKING_ENABLED = True

    with patch("opencopilot.analytics._track_copilot_start") as mock:
        track("copilot_start")

    assert mock.called
    