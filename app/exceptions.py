class ResourceNotFoundError(Exception):
    """Exception raised when a resource is not found."""
    def __init__(self, message="Resource not found"):
        self.message = message
        super().__init__(self.message)

class InvalidInputError(Exception):
    """Exception raised for invalid input."""
    def __init__(self, message="Invalid input provided"):
        self.message = message
        super().__init__(self.message)

class DatabaseError(Exception):
    """Exception raised for database-related errors."""
    def __init__(self, message="A database error occurred"):
        self.message = message
        super().__init__(self.message)