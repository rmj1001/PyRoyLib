class ResultException[E](Exception):
    """Custom exception for Result type"""

    def __init__(self, message: E) -> None:
        self.message = message
        super().__init__(self.message)
