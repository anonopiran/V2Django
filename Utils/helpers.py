import socket

NUMERIC_UNITS = ("k", "m", "g", "t", "p", "e", "z", "y")


def size__hr_to_bytes(val: str):
    val = val.lower().rstrip("b")
    if val.replace(".", "").isnumeric():
        val = int(float(val))
    else:
        val = float(val[:-1]) * 1024 ** (NUMERIC_UNITS.index(val[-1]) + 1)
    return val


def size__bytes_to_hr(num, suffix="B"):
    for unit in ("", *NUMERIC_UNITS[:-1]):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit.upper()}{suffix}"
        num /= 1024.0
    return f"{num:.1f}{NUMERIC_UNITS[-1].upper()}{suffix}"


def size__assert_bytes(val):
    if isinstance(val, str):
        val = size__hr_to_bytes(val)
    return val


def strip_port(addr: str):
    if ":" in addr:
        addr = addr[: addr.index(":")]
    return addr


def is_ip(addr: str):
    try:
        socket.inet_aton(strip_port(addr))
        return True
    except socket.error:
        return False
