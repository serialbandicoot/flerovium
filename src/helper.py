import random
import string


def random_string():
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(10))


def strip(value: str):
    if value is not None:
        return value.strip()
