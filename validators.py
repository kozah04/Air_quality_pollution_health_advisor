import re

def is_valid_location_name(text):
    # only letters, spaces, commas and hyphens allowed
    if not text:
        return False
    text = text.strip()
    pattern = r'^[A-Za-z\s,\-]+$'
    return bool(re.match(pattern, text))


def is_valid_coordinates(text):
    # checks something like "9.0765, 7.3986"
    pattern = r'^\s*-?\d{1,3}(\.\d+)?\s*,\s*-?\d{1,3}(\.\d+)?\s*$'
    return bool(re.match(pattern, text))


def extract_numbers(text):
    pattern = r'-?\d+\.?\d*'
    return re.findall(pattern, text)


def is_valid_date(text):
    # expects YYYY-MM-DD
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, text))
