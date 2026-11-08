class OptionException[E](Exception):
    """Custom exception for Option type"""

    def __init__(self, message: E) -> None:
        self.message = message
        super().__init__(self.message)
