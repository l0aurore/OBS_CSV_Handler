"""CSV handler module for the OBS CSV Updater plugin."""

import pandas as pd
import os
from typing import Dict, Optional, Union
from background_scripts.logger import logger
from background_scripts.config import CSV_ENCODING
from background_scripts.hex_converter import validate_hex_color  # Importing standalone hex validator

class CSVHandler:
    def __init__(self, csv_path):
        """Initialize the CSV handler with the path to the CSV file."""
        self.csv_path = csv_path
        self.last_data = None
        self.column_mapping = {}  # Maps CSV columns to OBS source names
        logger.info(f"Initialized CSV handler for: {csv_path}")

    def set_csv_path(self, new_path: str) -> bool:
        """Update the CSV file path and reset the last data."""
        try:
            if os.path.exists(new_path):
                self.csv_path = new_path
                self.last_data = None  # Reset last data to force update
                logger.info(f"Updated CSV path to: {new_path}")
                return True
            else:
                logger.error(f"CSV file not found: {new_path}")
                return False
        except Exception as e:
            logger.error(f"Error updating CSV path: {str(e)}")
            return False

    def set_column_mapping(self, mapping: Dict[str, str]):
        """Set the mapping between CSV columns and OBS source names."""
        self.column_mapping = mapping
        logger.info(f"Updated column mapping: {mapping}")

    def validate_file_path(self, path: str) -> str:
        """Validate and normalize file path."""
        if not path:
            return ""

        # Convert to absolute path if relative
        if not os.path.isabs(path):
            path = os.path.abspath(os.path.join(os.path.dirname(self.csv_path), path))

        # Verify file exists
        if not os.path.exists(path):
            logger.warning(f"File not found: {path}")
            return ""

        return path

    def process_special_columns(self, value: str, column_name: str) -> Union[str, int]:
        """Process special column types (file paths, hex colors)."""
        value = str(value).strip()  # Ensure value is a string and remove whitespace

        # Skip empty values
        if not value:
            return ""

        if '_picture' in column_name.lower() or '_image' in column_name.lower():
            return self.validate_file_path(value)
        elif '_hex' in column_name.lower() or '_color' in column_name.lower():
            # Call the imported validate_hex_color function
            color = validate_hex_color(value)
            if color is None:
                logger.warning(f"Invalid hex color: {value}")
                return 0  # Return default color (black) if invalid
            return color  # Return the ARGB decimal value
        return value

    def read_csv(self, update_last=True) -> Optional[Dict[str, Union[str, int]]]:
        """Read and parse the CSV file using column mappings."""
        try:
            logger.debug(f"Reading CSV file: {self.csv_path}")
            df = pd.read_csv(self.csv_path, encoding=CSV_ENCODING)

            if df.empty:
                logger.error("CSV file is empty")
                return None

            if not self.column_mapping:
                logger.info("No column mapping set. Please configure mapping in the GUI.")
                return {}

            source_updates = {}
            for source_name, csv_column in self.column_mapping.items():
                if csv_column in df.columns:
                    try:
                        value = df[csv_column].iloc[0]
                        processed_value = self.process_special_columns(value, csv_column)
                        source_updates[source_name] = processed_value
                        logger.debug(f"Processed column '{csv_column}' with value: {processed_value}")
                    except Exception as e:
                        logger.error(f"Error processing column '{csv_column}': {str(e)}")
                else:
                    logger.warning(f"Mapped column '{csv_column}' not found in CSV")

            if update_last and source_updates:
                self.last_data = source_updates.copy()
                logger.debug(f"Updated last_data with new values: {source_updates}")

            return source_updates

        except FileNotFoundError:
            logger.error(f"CSV file not found: {self.csv_path}")
            return None
        except pd.errors.EmptyDataError:
            logger.error(f"CSV file is empty: {self.csv_path}")
            return None
        except Exception as e:
            logger.error(f"Error reading CSV file: {str(e)}")
            return None


    def has_changes(self) -> bool:
        """Check if the CSV file has changed since last read."""
        current_data = self.read_csv(update_last=False)
        if current_data is None:
            return False

        has_changed = (self.last_data != current_data)
        if has_changed:
            logger.debug(f"Detected changes in CSV data. Old: {self.last_data}, New: {current_data}")

        return has_changed

    def get_available_columns(self) -> list:
        """Get list of available columns in the CSV file."""
        try:
            logger.info(f"Reading CSV file for columns: {self.csv_path}")
            df = pd.read_csv(self.csv_path, encoding=CSV_ENCODING)

            if df.empty:
                logger.warning("CSV file is empty")
                return []

            columns = list(df.columns)
            if not columns:
                logger.warning("No columns found in CSV file")
                return []

            logger.info(f"Found {len(columns)} columns in CSV: {columns}")
            return columns

        except pd.errors.EmptyDataError:
            logger.error(f"CSV file is empty: {self.csv_path}")
            return []
        except Exception as e:
            logger.error(f"Error getting CSV columns: {str(e)}")
            return []