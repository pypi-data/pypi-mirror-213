#
# (C) Eithery Lab, 2023
# Defines custom exceptions
#
class InvalidResultException(Exception):
    def __init__(self, message: str = "Invalid Result value"):
        super().__init__(message)
