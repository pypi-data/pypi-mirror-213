from __future__ import annotations

import logging

default_handler = logging.StreamHandler()
default_handler.setFormatter(logging.Formatter("{asctime} [{levelname!s:<8}] {message!s}", style="{"))


def create_logger(debug: bool = False) -> logging.Logger:
    """
    Get the app's logger and configure it if needed.
    """
    logger = logging.getLogger(__package__)

    if debug and not logger.level:
        logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        logger.addHandler(default_handler)

    return logger
