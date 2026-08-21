"""Random quiz mode: presents cards in a shuffled order."""

import random
from typing import List, Optional

from models import Flashcard
from quiz_modes.base import QuizMode


class RandomMode(QuizMode):
    """Presents flashcards in a randomised order."""

    def __init__(self, cards: List[Flashcard], seed: Optional[int] = None) -> None:
        """Initialise with a shuffled copy of the flashcard list.

        Args:
            cards: Flashcards to quiz in random order.
            seed: Optional RNG seed for deterministic behaviour in tests.
        """
        rng = random.Random(seed)
        self._cards = list(cards)
        rng.shuffle(self._cards)
        self._index = 0

    def next_card(self) -> Optional[Flashcard]:
        """Return the next randomly-ordered card, or None if all are done."""
        if self._index >= len(self._cards):
            return None
        card = self._cards[self._index]
        self._index += 1
        return card

    def mark_answer(self, card: Flashcard, correct: bool) -> None:
        """No special handling needed for random mode."""

    def has_remaining(self) -> bool:
        """Return True while there are unvisited cards."""
        return self._index < len(self._cards)
