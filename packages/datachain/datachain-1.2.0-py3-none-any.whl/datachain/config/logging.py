"""@Author: Rayane AMROUCHE

Logger class.
"""

from __future__ import annotations

import os
import logging
import datetime
import functools

from typing import Any


class Logger:
    """Logger class."""
    logger = None
    console = False
    paths = [] # type: list

    @classmethod
    def init_logger(cls) -> None:
        """Initializes a logger with the name 'datachain', removes any existing
        handlers, and sets the logging level to INFO.
        """
        cls.logger = logging.getLogger("datachain")
        handlers = cls.logger.handlers[:]
        for handler in handlers:
            cls.logger.removeHandler(handler)
            handler.close()
        cls.logger.setLevel(logging.INFO)
        cls.console = False
        cls.paths = []

    @classmethod
    def add_file(cls, path: str) -> None:
        """
        Creates a file handler for logging to a file at the specified path, sets a
        formatter for the log entries, and adds the file handler to the 'datachain'
        logger.

        Args:
            path: A string representing the path to the log file.
        """
        if path in cls.paths:
            return
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%a, %d %b %Y %H:%M:%S",
        )
        os.makedirs(path, exist_ok=True)
        file_handler = logging.FileHandler(os.path.join(path, "datachain.log"))
        file_handler.setFormatter(formatter)
        if cls.logger:
            cls.logger.addHandler(file_handler)
        cls.paths.append(path)

    @classmethod
    def add_console(cls) -> None:
        """Initializes a console handler and adds it to the 'datachain' logger."""
        if cls.console:
            return
        console_handler = logging.StreamHandler()
        if cls.logger:
            cls.logger.addHandler(console_handler)
        cls.console = True

    @staticmethod
    def log_func(func: Any) -> Any:
        """
        A decorator function that logs the execution time of a function.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwds):
            tic = datetime.datetime.now()
            result = None
            raise_err = False
            try:
                result = func(*args, **kwds)
            except Exception as err:  # pylint: disable=broad-except
                result = err
                raise_err = True
            time_taken = str(datetime.datetime.now() - tic)
            msg = f"Executed '{func.__qualname__}' in {time_taken}s."
            if raise_err:
                Logger.logger.warning(msg)
                raise result
            Logger.logger.info(msg)
            return result

        return wrapper
