"""Configuration settings for the OBS CSV Updater plugin."""

import os

# Get the directory where config.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Testing mode
TESTING_MODE = False  # Set to False when using with real OBS

# OBS WebSocket connection settings
OBS_HOST = "10.0.0.41"  # 
OBS_PORT = 4455
# Set to None or empty string for non-authenticated connections
OBS_PASSWORD = None

# Connection retry settings
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# CSV settings
DEFAULT_CSV_PATH = os.path.join(BASE_DIR, "data.csv")
CSV_ENCODING = "utf-8"

# Update settings
UPDATE_INTERVAL = 1.0  # seconds

# Logging settings
LOG_FILE = os.path.join(BASE_DIR, "obs_csv_updater.log")
LOG_LEVEL = "INFO"
