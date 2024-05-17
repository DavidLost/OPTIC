def to_1337_speak(text: str):
    """Convert a string to leet speak."""
    leet_dict = str.maketrans({
        'a': '4', 'b': '8', 'e': '3', 'g': '6', 'i': '1', 'l': '1',
        'o': '0', 's': '5', 't': '7', 'z': '2', 'A': '4', 'B': '8',
        'E': '3', 'G': '6', 'I': '1', 'L': '1', 'O': '0', 'S': '5',
        'T': '7', 'Z': '2'
    })
    return text.translate(leet_dict)