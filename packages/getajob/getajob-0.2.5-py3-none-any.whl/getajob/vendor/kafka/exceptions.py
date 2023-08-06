class InvalidTokenException(Exception):
    def __init__(self, message="Invalid token"):
        self.message = message
        super().__init__(self.message)


class ExpiredTokenException(Exception):
    def __init__(self, message="Expired token"):
        self.message = message
        super().__init__(self.message)
