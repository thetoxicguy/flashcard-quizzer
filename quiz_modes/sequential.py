"""Sequential quiz mode: presents cards in original file order."""

from typing import List, Optional

from models import Flashcard
from quiz_modes.base import QuizMode


class SequentialMode(QuizMode):
    """Presents flashcards one by one in the order they appear in the file."""

    def __init__(self, cards: List[Flashcard]) -> None:
        """Initialise with a list of flashcards.

        Args:
            cards: Ordered list of flashcards to quiz.
        """
        self._cards = list(cards)
        self._index = 0

    def next_card(self) -> Optional[Flashcard]:
        """Return the next card in sequence, or None if all cards are done."""
        if self._index >= len(self._cards):
            return None
        card = self._cards[self._index]
        self._index += 1
        return card

    def mark_answer(self, card: Flashcard, correct: bool) -> None:
        """No special handling needed for sequential mode."""

    def has_remaining(self) -> bool:
        """Return True while there are unvisited cards."""
        return self._index < len(self._cards)
