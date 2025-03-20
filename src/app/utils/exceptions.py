class NotFoundError(Exception):
    """Exception raised when a requested resource is not found."""

    def __init__(self, entity: str, message: str = "%s not found."):
        self.message = message % entity
        super().__init__(self.message)
