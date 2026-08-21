"""Domain models for Flashcard Quizzer."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Flashcard:
    """Represents a single flashcard with a front (question) and back (answer)."""

    front: str
    back: str


@dataclass
class SessionStats:
    """Tracks statistics for a single quiz session."""

    total: int = 0
    correct: int = 0
    missed: List[str] = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        """Return accuracy as a percentage (0.0–100.0)."""
        if self.total == 0:
            return 0.0
        return (self.correct / self.total) * 100.0
