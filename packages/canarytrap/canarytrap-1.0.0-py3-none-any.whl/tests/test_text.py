import canarytrap as canary
import random


def test_unicode_space_encode_count():
    random.seed(0)
    text = "This is the text to test"
    encoded_text, binary_string = canary.text.unicode_space_encode(text)
    bin_pos_count = binary_string.count('1')
    blank_space_count = encoded_text.count("\u200E")
    assert bin_pos_count == blank_space_count
    

def test_unicode_space_encode_position():
    random.seed(0)
    text = "This is the text to test"
    encoded_text, binary_string = canary.text.unicode_space_encode(text)

    calculated_binary_string = ""
    for i, char in enumerate(encoded_text):
        if char == "\u200E":
            calculated_binary_string += "1"
        elif char == " ":
            calculated_binary_string += "0"
    
    assert binary_string == calculated_binary_string


def test_unicode_space_to_binary_str():
    random.seed(0)
    text = "This is the text to test"
    encoded_text, binary_str = canary.text.unicode_space_encode(text)
    calculated_binary = canary.text.unicode_space_to_binary_str(encoded_text)
    assert binary_str == calculated_binary


def test_unicode_space_match():
    random.seed(0)
    text = "This is the text to test"
    encoded_text, binary_string = canary.text.unicode_space_encode(text)
    assert canary.text.unicode_space_match(encoded_text, binary_string) == 1.0