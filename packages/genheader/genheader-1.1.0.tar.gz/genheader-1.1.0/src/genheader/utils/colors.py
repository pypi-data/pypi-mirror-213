#!/usr/bin/env python3

from dataclasses import dataclass

# Dataclass to store color codes
@dataclass(frozen=True)
class ColorCodes:
    RED = "\033[91m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    GREY = "\033[90m"
    BLACK = "\033[90m"
    DEFAULT = "\033[99m"
    END = "\033[0m"


# Function to apply color to a string
def cstr(color: str, string: str):
    return f"{getattr(ColorCodes, color.upper())}{string}{ColorCodes.END}"


# Function to print colored string
def cprint(color: str, string: str):
    print(cstr(color, string))
