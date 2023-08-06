MAIN_PART_PATTERN: str = r"^((\w+)?(\/)?(\w+)?(\(\w+\))?(\!)?:)?(.+)$"
"""
The main part of Conventional Message consists of meta information and
arbitrary text with tags.

Groups:
    0: meta information, groups 1-4 are stored inside
    1: project
    2: separation `/`
    3: type
    4: module
    5: breaking mark
    6: text

Note that on meta information group searching failure, everything is going to
be written in group #5, which is desired, for example at
`orwynn/re-fa-c-tor: mytext`.
"""

TAG_PATTERN: str = r"#[^\d]\w+"

FUTURE_RESERVED_OPERATOR_PATTERNS: list[str] = [
    r"\+\+",
    r"&\w+",
    r"\-\>",
    r"\<\-",
    r"&&",
    r"\|\|",
    r"\$\w+"
]

CONSECUTIVE_SPACES_PATTERN: str = r"\s{2,}"
