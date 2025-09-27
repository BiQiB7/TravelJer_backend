"""
This module provides a customized logging setup for the design agent.

The `Logger` class is a singleton that provides a consistent logging interface throughout the application. It creates a new logger instance for each design ID, ensuring that logs for different designs are kept separate.
"""
import logging
import os
import time
from logging.handlers import RotatingFileHandler


class Logger:
    """
    A singleton class for creating and managing loggers.

    This class ensures that a single logger instance is created for each design ID, providing a consistent logging interface throughout the application.
    """
    _instances = {}

    def __new__(cls, logger_id=None):
        """
        Creates a new logger instance for each design ID or returns an existing one.

        Args:
            logger_id: A unique identifier for the design.

        Returns:
            A logger instance.
        """
        # Create a new logger instance for each logger_id or return existing one
        if logger_id not in cls._instances:
            instance = super(Logger, cls).__new__(cls)
            instance._initialize_logger(logger_id)
            cls._instances[logger_id] = instance
        return cls._instances[logger_id]

    def _initialize_logger(self, logger_id=None):
        """
        Initializes a new logger instance.

        Args:
            logger_id: A unique identifier for the design.
        """
        if logger_id is not None:
            os.makedirs(f'{logger_id}',exist_ok=True)
        if logger_id:
            log_filename = f"{logger_id}/log.log"
        else:
            log_filename = f"logs/log_{time.strftime('%Y%m%d_%H%M%S')}.log"
        logger_name = logger_id if logger_id else "LOGGER"
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)

        self.logger.handlers = []
        file_handler = RotatingFileHandler(
            log_filename,
            maxBytes=1024*1024,  # 1MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",
            datefmt="%H:%M:%S"
        ))
        self.logger.addHandler(file_handler)
        self.logger.propagate = False
        self.logger_id = logger_id

    def get_logger(self):
        """
        Returns the logger instance.

        Returns:
            A logger instance.
        """
        return self.logger
        