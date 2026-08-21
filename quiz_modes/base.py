"""Abstract base class defining the QuizMode strategy interface."""

from abc import ABC, abstractmethod
from typing import Optional

from models import Flashcard


class QuizMode(ABC):
    """Strategy interface for quiz card ordering and repetition logic."""

    @abstractmethod
    def next_card(self) -> Optional[Flashcard]:
        """Return the next card to present, or None if the session is complete.

        Returns:
            The next Flashcard, or None when no cards remain.
        """

    @abstractmethod
    def mark_answer(self, card: Flashcard, correct: bool) -> None:
        """Record the result of an answered card.

        Args:
            card: The card that was answered.
            correct: True if the user answered correctly, False otherwise.
        """

    @abstractmethod
    def has_remaining(self) -> bool:
        """Return True if there are more cards to present in this session.

        Returns:
            True when cards remain, False when the session is complete.
        """
