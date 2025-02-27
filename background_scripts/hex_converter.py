from background_scripts.padding_hex import format_hex # Ensure padding_hex.py contains format_hex

def validate_hex_color(hex_value):
    """
    Convert a hex color string to OBS-compatible BGRA decimal integer.
    Handles both 6-digit RGB (#RRGGBB) and 8-digit RGBA (#RRGGBBAA) hex codes.
    Also preserves existing decimal RGBA values.

    Args:
        hex_value (str): Hex color string with or without leading '#',
                        in either RRGGBB or RRGGBBAA format,
                        or a decimal RGBA integer as a string.

    Returns:
        int: BGRA decimal integer suitable for OBS color sources,
             or None if the input is invalid.
    """
    try:
        # Remove quotes, whitespace, and handle empty input
        hex_value = str(hex_value).strip().strip('"\'')
        if not hex_value:
            return None

        # Handle decimal values first (preserve existing BGRA values)
        if hex_value.isdigit() and len(hex_value) > 8:
            decimal_value = int(hex_value)
            if 0 <= decimal_value <= 0xFFFFFFFF:  # Valid 32-bit color range
                return decimal_value

        # Handle special case for "0" input (black color)
        if hex_value == "0":
            return 0xFF000000  # Black with full alpha

        # Remove the leading '#' if present
        hex_value = hex_value.lstrip('#')

        # Validate hex characters (case-insensitive)
        if not all(c in '0123456789ABCDEFabcdef' for c in hex_value):
            return None

        # Convert to uppercase for consistency
        hex_value = hex_value.upper()

        # Ensure the hex value is exactly 6 or 8 characters long
        hex_value = padding_hex.format_hex(hex_value, 6)  # Calls format_hex to adjust length
        
        if not hex_value:  # If format_hex returned None, the input was invalid
            return None

        # Convert hex string to integer values
        try:
            # Extract color components in reverse order for BGRA
            r = int(hex_value[2:4], 16)  # Read red
            g = int(hex_value[4:6], 16)  # Green
            b = int(hex_value[6:8], 16)  # Blue
            a = int(hex_value[8:10], 16)  # Alpha

            # Pack as BGRA for OBS (correct byte order)
            result = (a << 24) | (b << 16) | (g << 8) | r

            return result

        except ValueError:
            return None  # Invalid hex digits

    except (ValueError, TypeError):
        return None
