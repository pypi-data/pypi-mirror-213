def replace(s: str, *chars: str) -> str:
    for c in chars:
        s = s.replace(c, "")

    return s
