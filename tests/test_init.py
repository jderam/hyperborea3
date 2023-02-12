import logging
import os
from unittest import mock

from hyperborea3 import get_debug, logger_setup


@mock.patch.dict(os.environ, {"HYPERBOREA3_DEBUG": "0"})
def test_get_debug_0():
    assert get_debug() is False


@mock.patch.dict(os.environ, {"HYPERBOREA3_DEBUG": "1"})
def test_get_debug_1():
    assert get_debug() is True


@mock.patch.dict(os.environ, {"HYPERBOREA3_DEBUG": "0"})
def test_logger_setup_0():
    logger = logger_setup()
    for handler in logger.handlers:
        assert isinstance(handler, logging.StreamHandler)
    assert logger.getEffectiveLevel() == 30


@mock.patch.dict(os.environ, {"HYPERBOREA3_DEBUG": "1"})
def test_logger_setup_1():
    logger = logger_setup()
    for handler in logger.handlers:
        assert any(
            [
                isinstance(handler, logging.FileHandler),
                isinstance(handler, logging.StreamHandler),
            ]
        )
    assert logger.getEffectiveLevel() == 10
