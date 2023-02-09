import logging
import os

__version__ = "0.5.4"

DEBUG = os.getenv("DEBUG", "0")

logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


if DEBUG == "1":
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    file_handler = logging.FileHandler("app.log")
    # file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.WARN)
console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.WARN)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
