"""Main script for the OBS CSV Updater plugin."""

import time
import signal
import sys
from config import (
    OBS_HOST,
    OBS_PORT,
    OBS_PASSWORD,
    DEFAULT_CSV_PATH,
    UPDATE_INTERVAL,
    TESTING_MODE
)
from csv_handler import CSVHandler
from obs_controller import OBSController
from file_watcher import FileWatcher
from logger import logger

class OBSCSVUpdater:
    def __init__(self):
        """Initialize the OBS CSV Updater plugin."""
        self.running = True
        self.csv_path = DEFAULT_CSV_PATH
        self.csv_handler = CSVHandler(self.csv_path)
        self.file_watcher = FileWatcher(self.csv_path)
        self.obs_controller = OBSController(OBS_HOST, OBS_PORT, OBS_PASSWORD)

    def set_csv_path(self, new_path):
        """Update the CSV file path and reinitialize handlers."""
        logger.info(f"Updating CSV path to: {new_path}")
        if self.csv_handler.set_csv_path(new_path) and self.file_watcher.set_file_path(new_path):
            self.csv_path = new_path
            logger.info("Successfully updated CSV path and reinitialized handlers")
            return True
        return False

    def setup_signal_handlers(self):
        """Set up signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            logger.info("Received shutdown signal, cleaning up...")
            self.running = False

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def run(self):
        """Main loop for the updater."""
        mode = "Testing" if TESTING_MODE else "Production"
        logger.info(f"Starting OBS CSV Updater in {mode} mode")

        # Connect to OBS
        if not self.obs_controller.connect():
            if not TESTING_MODE:
                logger.error("Failed to connect to OBS. Exiting.")
                return
            else:
                logger.warning("Failed to connect to OBS, but continuing in testing mode")

        # Initial CSV read
        initial_data = self.csv_handler.read_csv()
        if initial_data:
            self.obs_controller.bulk_update_sources(initial_data)

        # Main update loop
        while self.running:
            try:
                # Check for file changes
                if self.file_watcher.check_for_changes():
                    logger.debug("File change detected, checking for data updates")
                    if self.csv_handler.has_changes():
                        # Read and update sources
                        updates = self.csv_handler.read_csv()
                        if updates:
                            if self.obs_controller.bulk_update_sources(updates):
                                logger.info("Successfully updated sources")
                            else:
                                logger.warning("Failed to update some sources")

                time.sleep(UPDATE_INTERVAL)

            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                time.sleep(UPDATE_INTERVAL)

        # Cleanup
        self.obs_controller.disconnect()
        logger.info("OBS CSV Updater stopped")

def main():
    """Entry point for the application."""
    updater = OBSCSVUpdater()
    updater.setup_signal_handlers()
    updater.run()

if __name__ == "__main__":
    main()