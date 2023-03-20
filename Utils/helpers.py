import socket

NUMERIC_UNITS = ("k", "m", "g", "t", "p", "e", "z", "y")


def size__hr_to_bytes(val: str):
    val = val.lower().rstrip("b")
    if val.replace(".", "").isnumeric():
        val = int(float(val))
    else:
        val = float(val[:-1]) * 1024 ** (NUMERIC_UNITS.index(val[-1]) + 1)
    return val


def size__assert_bytes(val):
    if isinstance(val, str):
        val = size__hr_to_bytes(val)
    return val
