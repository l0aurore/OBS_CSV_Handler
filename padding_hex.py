#padding_hex

def format_hex(hex_value, total_length=6):
    hex_str = hex_value.lstrip("0x")  # Remove "0x" if it exists
    
    # Ensure it's at least 6 characters long
    if len(hex_str) < 6:
        hex_str = hex_str.zfill(6)  # Pad with leading zeros to reach 6 digits

    # Convert 6-digit to 8-digit by adding 'FF'
    if len(hex_str) == 6:
        hex_str += "FF"
    elif len(hex_str) != 8:
        return None  # Invalid length

    num_zeros = total_length - len(hex_str) - 2  # Adjust for "0x"
    
    if num_zeros > 0:
        hex_value = f"0x{'0' * num_zeros}{hex_str}"  # Overwrite hex_value
    else:
        hex_value = f"0x{hex_str}"

    return hex_value  # Now hex_value is updated
"""
hex_value = "33550"
hex_value = format_hex(hex_value, 6)  # Overwrite hex_value with the formatted version
print(hex_value)  # Output: 0x0000ABCD

def process_hex(hex_value):
    try:
        # Extract color components in reverse order for BGRA
        r = int(hex_value[0:2], 16)  # Read red
        g = int(hex_value[2:4], 16)  # Green
        b = int(hex_value[4:6], 16)  # Blue
        a = int(hex_value[6:8], 16)  # Alpha

        # Pack as BGRA for OBS (correct byte order)
        result = (a << 24) | (b << 16) | (g << 8) | r

        return result

    except ValueError:
        return None  # Invalid hex digits
"""
