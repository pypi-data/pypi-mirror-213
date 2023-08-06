"""
Canary Trap for text
"""
from typing import Tuple
from random import randint


def unicode_space_encode(text:str, binary_string:str|None = None) -> Tuple[str, str]:
    """ Encode spaces in text to unicode spaces based on a binary value

    If the text has 12 spaces and the binary value is 1100, then the first 2 spaces will be unicode spaces.
    If no binary value is provided, then the binary value is randomized

    Args:
        text: The text to encode
        binary: The binary value to use. Each 1 means a replacement of a space char with a blank char. 
        Defaults to None.

    Returns:
        The encoded text and the binary value used

    Raises:
        ValueError: If the binary value (in terms of string length) is too large for the number of spaces in the text
    """
    blank_space = "\u200E"
    space_count = text.count(" ")
    space_indicies = [i for i, char in enumerate(text) if char == " "]

    if binary_string is None:
        binary = randint(0, 2**space_count - 1)
        binary_string = bin(binary)[2:]

    if len(binary_string) > space_count:
        raise ValueError("The length of the binary string is too large for the number of spaces in the text")

    # For all instances of '1', replcae the next space
    text_list = list(text)
    for i, space_index in zip(range(len(binary_string)), space_indicies):
        if binary_string[i] == '1':
            text_list[space_index] = blank_space
    
    text = "".join(text_list)
    text = text.replace(blank_space, f"{blank_space} ")
    binary_string = unicode_space_to_binary_str(text)
    return text, binary_string


def unicode_space_to_binary_str(text:str) -> str:
    """ Convert unicode spaces to binary

    Args:
        text: The text to convert

    Returns:
        The binary string
    """
    blank_space = "\u200E"
    binary_string = ""
    
    skip_next = False 
    for char in text:
        if skip_next:
            skip_next = False
            continue
        if char == blank_space:
            binary_string += "1"
            skip_next = True
        elif char == " ":
            binary_string += "0"
    
    return binary_string


def unicode_space_match(text:str, binary_str:str) -> float:
    """ Check if the text matches the binary value

    Args:
        text: The text to check
        binary_str: The binary value to check against

    Returns:
        The percentage of spaces that match the binary value
    
    Example:
        >>> text = "Hello world[unicode]this[unicode]is text"
        >>> binary = 0b0101 # Only half the values match where the unicode is
        >>> unicode_space_match(text, binary) 
        0.5
    """
    blank_space = "\u200E"
    text = text.replace(f"{blank_space} ", blank_space)
    space_count = text.count(" ") + text.count(blank_space)
    space_indicies = [i for i, char in enumerate(text) if char == " " or char == blank_space]

    match_count = 0
    for bin_val, space_index in zip(binary_str, space_indicies):
        if bin_val == '1' and text[space_index] == blank_space:
            match_count += 1
        elif bin_val == '0' and text[space_index] == " ":
            match_count += 1
    
    return match_count / space_count


