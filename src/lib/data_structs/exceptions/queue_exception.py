class QueueException(Exception):
    """Exception raised when queue operations fail"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
