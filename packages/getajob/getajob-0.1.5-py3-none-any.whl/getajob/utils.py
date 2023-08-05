import typing as t
import random
import string


def generate_random_short_code():
    return "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(10)
    )


def string_to_bool(string_in: t.Optional[str] = None) -> bool:
    if string_in is None:
        return False
    if string_in.lower() == "true":
        return True
    return False
