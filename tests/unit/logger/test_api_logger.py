from unittest.mock import MagicMock

from opencopilot.logger import api_logger

logger = None


def setup_function():
    global logger
    logger = MagicMock()
    logging = MagicMock()
    logging.getLogger.return_value = logger
    api_logger.logging = logging


def test_set_log_level_none():
    api_logger.set_log_level(None)
    logger.setLevel.assert_called_with(20)


def test_set_log_level_1():
    api_logger.set_log_level(1)
    logger.setLevel.assert_called_with(1)


def test_set_log_level_negative():
    api_logger.set_log_level(-1)
    logger.setLevel.assert_called_with(-1)


def test_set_log_level_valid_string():
    api_logger.set_log_level("debug")
    logger.setLevel.assert_called_with(10)


def test_set_log_level_invalid_string():
    api_logger.set_log_level("invalid")
    logger.setLevel.assert_called_with(20)
