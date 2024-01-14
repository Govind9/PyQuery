class UnexpectedTokenError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"Unexpected Token Error: {message}")


class ExecutionError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"Execution Error: {message}")
