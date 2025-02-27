"""File watcher module for the OBS CSV Updater plugin."""

import os
import time
from logger import logger

class FileWatcher:
    def __init__(self, file_path):
        """Initialize the file watcher with a file path."""
        self.file_path = file_path
        self.last_modified = self._get_modified_time()
        logger.debug(f"Initialized file watcher for: {file_path}")

    def _get_modified_time(self):
        """Get the last modified time of the file."""
        try:
            if os.path.exists(self.file_path):
                return os.path.getmtime(self.file_path)
            return 0
        except Exception as e:
            logger.error(f"Error getting modified time for {self.file_path}: {str(e)}")
            return 0

    def check_for_changes(self):
        """Check if the file has been modified since last check."""
        try:
            current_modified = self._get_modified_time()
            if current_modified > self.last_modified:
                self.last_modified = current_modified
                logger.debug(f"Detected change in file: {self.file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error checking for changes: {str(e)}")
            return False

    def set_file_path(self, new_path):
        """Update the file path being watched."""
        try:
            if os.path.exists(new_path):
                self.file_path = new_path
                self.last_modified = self._get_modified_time()
                logger.info(f"Updated file path to: {new_path}")
                return True
            else:
                logger.error(f"File not found: {new_path}")
                return False
        except Exception as e:
            logger.error(f"Error setting file path: {str(e)}")
            return False
