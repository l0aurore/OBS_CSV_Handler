import time
import obsws_python as obs
from background_scripts.logger import logger
from background_scripts.config import MAX_RETRIES, RETRY_DELAY
from background_scripts.hex_converter import validate_hex_color  # Import the hex converter function

class OBSController:
    def __init__(self, host, port, password=None):
        """Initialize the OBS WebSocket connection."""
        self.host = host
        self.port = port
        self.password = password if password else None  # Convert empty string to None
        self.client = None
        logger.info(f"Initializing OBS Controller with host={host}, port={port}, using authentication: {bool(self.password)}")

    def connect(self):
        """
        Establish connection to OBS WebSocket server with retry mechanism.
        Returns True if connection successful, False otherwise.
        """
        for attempt in range(MAX_RETRIES):
            try:
                logger.info(f"Attempting to connect to OBS WebSocket (attempt {attempt + 1}/{MAX_RETRIES})")
                logger.debug(f"Connection details - Host: {self.host}, Port: {self.port}, Using authentication: {bool(self.password)}")

                self.client = obs.ReqClient(
                    host=self.host,
                    port=self.port,
                    password=self.password
                )

                # Test the connection with a simple request
                version = self.client.get_version()
                logger.info(f"Successfully connected to OBS WebSocket (OBS Version: {version.obs_version})")
                return True

            except ConnectionRefusedError:
                logger.warning(
                    f"Connection refused (attempt {attempt + 1}/{MAX_RETRIES}). "
                    "Make sure OBS is running and WebSocket server is enabled in Tools -> WebSocket Server Settings"
                )
            except Exception as e:
                logger.error(f"Failed to connect to OBS (attempt {attempt + 1}/{MAX_RETRIES})")
                logger.error(f"Error details: {str(e)}")
                logger.error(f"Error type: {type(e).__name__}")

            if attempt < MAX_RETRIES - 1:
                logger.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)

        logger.error(
            "Failed to connect to OBS after multiple attempts. "
            "Please check that:\n"
            "1. OBS is running\n"
            "2. WebSocket server is enabled in OBS (Tools -> WebSocket Server Settings)\n"
            "3. The port matches your OBS WebSocket settings\n"
            "4. WebSocket server authentication is disabled in OBS settings\n"
            "5. Windows Firewall is allowing connections on port 4455"
        )
        return False

    def source_exists(self, source_name):
        """Check if a source exists in OBS."""
        if not self.client:
            logger.error("Not connected to OBS")
            return False

        try:
            self.client.get_input_settings(source_name)
            return True
        except Exception as e:
            logger.debug(f"Source '{source_name}' does not exist: {str(e)}")
            return False

    def create_text_source(self, source_name, initial_text=""):
        """Create a new text source in OBS."""
        if not self.client:
            logger.error("Not connected to OBS")
            return False

        try:
            # First ensure we have a scene
            scenes_response = self.client.get_scene_list()
            scene_name = None

            # Check if we have any scenes
            if hasattr(scenes_response, 'scenes') and scenes_response.scenes:
                # Get the first scene from the list
                scene_name = scenes_response.scenes[0]['sceneName']
            else:
                # Create a new scene if none exists
                scene_name = "Scene"
                try:
                    self.client.create_scene(scene_name)
                    logger.info(f"Created new scene: {scene_name}")
                except Exception as e:
                    logger.error(f"Failed to create scene: {str(e)}")
                    return False

            # Determine input kind based on source name
            input_kind = "text_ft2_source_v2"  # default
            input_settings = {"text": str(initial_text)}

            if "picture" in source_name.lower():
                input_kind = "image_source"
                input_settings = {"file": str(initial_text)}
            elif "color" in source_name.lower():
                input_kind = "color_source_v3"
                # Use validate_hex_color for color validation
                color = validate_hex_color(str(initial_text))
                if not color:
                    logger.error(f"Invalid color format for source '{source_name}' with value '{initial_text}'")
                    return False  # Return false if the color is invalid
                input_settings = {"color": color}
            elif "browser" in source_name.lower():
                input_kind = "browser_source"
                input_settings = {"url": str(initial_text)}
            elif "media" in source_name.lower():
                input_kind = "ffmpeg_source"
                input_settings = {"local_file": str(initial_text)}

            self.client.create_input(
                sceneName=scene_name,
                inputName=source_name,
                inputKind=input_kind,
                inputSettings=input_settings,
                sceneItemEnabled=True
            )
            logger.info(f"Created new text source: {source_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to create text source '{source_name}': {str(e)}")
            return False


    def update_source(self, source_name, value):
        """Update an OBS text source with new value. Create if doesn't exist."""
        if not self.client:
            logger.error("Not connected to OBS")
            return False

        try:
            # Check if source exists, create if it doesn't
            if not self.source_exists(source_name):
                logger.info(f"Source '{source_name}' doesn't exist, creating it...")
                if not self.create_text_source(source_name, str(value)):
                    return False

            # Determine settings based on source name
            new_settings = {"text": str(value)}  # default

            if "picture" in source_name.lower():
                new_settings = {"file": str(value)}
            elif "color" in source_name.lower():
                # Use validate_hex_color for color validation
                color = validate_hex_color(str(value))
                if not color:
                    logger.error(f"Invalid color format for source '{source_name}' with value '{value}'")
                    return False  # Return false if color is invalid
                new_settings = {"color": color}
            elif "browser" in source_name.lower():
                new_settings = {"url": str(value)}
            elif "media" in source_name.lower():
                new_settings = {"local_file": str(value)}

            self.client.set_input_settings(source_name, new_settings, True)

            logger.info(f"Updated source '{source_name}' with value: {value}")
            return True
        except Exception as e:
            logger.error(f"Failed to update source '{source_name}': {str(e)}")
            return False

    def bulk_update_sources(self, updates):
        """
        Update multiple OBS sources at once. Create any that don't exist.

        Args:
            updates (dict): Dictionary of source names and their new values
        """
        if not self.client:
            logger.error("Not connected to OBS")
            return False

        success = True
        for source_name, value in updates.items():
            if not self.update_source(source_name, value):
                success = False
        return success

    def disconnect(self):
        """Disconnect from OBS WebSocket server."""
        try:
            if self.client:
                self.client = None
            logger.info("Disconnected from OBS WebSocket")
        except Exception as e:
            logger.error(f"Error disconnecting from OBS: {str(e)}")
