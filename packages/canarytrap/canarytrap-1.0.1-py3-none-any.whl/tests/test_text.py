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
    skip_next = False
    for i, char in enumerate(encoded_text):
        if skip_next:
            skip_next = False
            continue
        if char == "\u200E":
            calculated_binary_string += "1"
            skip_next = True
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


def test_unicode_space_match_leading_0():
    random.seed(0)
    text = f"Hello\u200e my\u200e name\u200e is Matthew Lee"
    wrong_bin = "111"
    corr_bin = "11100"
    assert canary.text.unicode_space_match(text, wrong_bin) <= 1.0
    assert canary.text.unicode_space_match(text, corr_bin) == 1.0