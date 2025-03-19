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