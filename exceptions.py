"""Custom application exceptions for Flashcard Quizzer."""


class FlashcardError(Exception):
    """Base exception for all Flashcard Quizzer errors."""


class FileLoadError(FlashcardError):
    """Raised when a flashcard file cannot be loaded or parsed."""


class ValidationError(FlashcardError):
    """Raised when flashcard data fails structural validation."""


class InvalidModeError(FlashcardError):
    """Raised when an unsupported quiz mode is requested."""
