"""
This module defines custom exception classes for the application.
"""


class ResumeProcessingError(Exception):
    """Base exception for resume processing errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class FileTypeError(ResumeProcessingError):
    """Exception raised for unsupported file types."""

    def __init__(self, message: str = "Unsupported file type"):
        super().__init__(message, status_code=415)


class ParsingError(ResumeProcessingError):
    """Exception raised for errors during resume parsing."""

    def __init__(self, message: str = "Failed to parse resume"):
        super().__init__(message, status_code=500)
