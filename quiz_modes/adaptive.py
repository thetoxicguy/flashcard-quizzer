"""Adaptive quiz mode: re-queues missed cards until answered correctly."""

from collections import deque
from typing import Deque, List, Optional

from models import Flashcard
from quiz_modes.base import QuizMode


class AdaptiveMode(QuizMode):
    """Presents cards and re-queues incorrect answers until all are mastered."""

    def __init__(self, cards: List[Flashcard]) -> None:
        """Initialise with the full list of flashcards.

        Args:
            cards: Flashcards to quiz adaptively.
        """
        self._queue: Deque[Flashcard] = deque(cards)

    def next_card(self) -> Optional[Flashcard]:
        """Return the next card from the queue, or None if the queue is empty."""
        if not self._queue:
            return None
        return self._queue.popleft()

    def mark_answer(self, card: Flashcard, correct: bool) -> None:
        """Re-queue the card if the answer was incorrect.

        Args:
            card: The card that was just answered.
            correct: True if the user was correct, False to re-queue the card.
        """
        if not correct:
            self._queue.append(card)

    def has_remaining(self) -> bool:
        """Return True while there are cards in the queue."""
        return bool(self._queue)
