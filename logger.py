"""Logging configuration for the OBS CSV Updater plugin."""

import logging
from logging.handlers import RotatingFileHandler
from config import LOG_FILE, LOG_LEVEL

def setup_logger():
    """Configure and return the logger instance."""
    logger = logging.getLogger('OBSCSVUpdater')
    logger.setLevel(getattr(logging, LOG_LEVEL))

    # Create handlers
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5
    )
    console_handler = logging.StreamHandler()

    # Create formatters and add it to handlers
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()
