class ParsingError(Exception):
    """
    Unable to parse a message.
    """


class MissingFieldError(Exception):
    """
    Field is missing.
    """
    def __init__(self, *, field: str) -> None:
        message: str = f"the field={field} is missing"
        super().__init__(message)


class ReservedOperatorError(Exception):
    """
    Some operator, i.e. char combination is reserved for future use.
    """
    def __init__(self, *, operator: str) -> None:
        message: str = f"operator={operator} is reserved for future use"
        super().__init__(message)
