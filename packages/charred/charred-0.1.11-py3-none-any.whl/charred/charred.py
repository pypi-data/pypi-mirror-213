"""

author: @endormi

Very simple char functions

"""


def is_ascii_char(input):
    if isinstance(input, str):
        # Check if the input character has an ASCII code between 0 and 127
        if 0 <= ord(input) < 128:
            return True
    return False


def is_same_char(char):
    return all(c == char[0] for c in char[1:])


def is_string(char):
    return type(char) == str


def is_unicode_char(input):
    if isinstance(input, str):
        # Encode the string as UTF-8 and check
        # if it contains non-ASCII characters
        if len(input.encode('utf-8')) > len(input):
            return True
    return False


def repeat_char(char, num_of_times):
    return (char * (num_of_times//len(char) + 1))[:num_of_times]
