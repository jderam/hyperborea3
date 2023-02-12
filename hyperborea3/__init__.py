import logging
import os

__version__ = "0.6.0"


def get_debug() -> bool:
    """Return debug=True if the environment variable HYPERBOREA3_DEBUG is set to 1."""
    hyperborea3_debug = os.getenv("HYPERBOREA3_DEBUG", "0")
    debug = True if hyperborea3_debug == "1" else False
    return debug


def logger_setup() -> logging.Logger:
    debug = get_debug()
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger_level = logging.DEBUG if debug else logging.WARNING

    logger.setLevel(logger_level)

    def _setup_file_handler(logger_level: int) -> None:
        file_handler = logging.FileHandler("app.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        file_handler.setLevel(logger_level)

    def _setup_console_handler(logger_level: int) -> None:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        console_handler.setLevel(logger_level)

    _setup_console_handler(logger_level)

    if debug:
        _setup_file_handler(logger_level)

    return logger


logger = logger_setup()
