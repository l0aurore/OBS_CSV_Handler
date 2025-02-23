"""Test script to verify hex color conversion for OBS."""
from hex_converter import validate_hex_color

def test_color(color, description=""):
    result = validate_hex_color(color)
    print(f"{description:20} Input: {color:10} -> Output: {result}")

# Test with actual values from data.csv
test_color("FF5733", "Player 1 Color")
test_color("#FF5733CC", "Player 2 Color")
test_color("CFAA4C", "Player 3 Color")

# Test with decimal values
test_color("4294924083", "Decimal ARGB")
test_color("3439286067", "Decimal w/Alpha")

# Test with problematic values
test_color("0.0", "Invalid decimal")
test_color("000000", "Black")
test_color("", "Empty string")
test_color("INVALID", "Invalid hex")