"""Quiz engine: factory, session orchestration, and statistics display."""

import dataclasses
from typing import Callable, Dict, Iterator, List, Optional, Tuple

from exceptions import InvalidModeError
from models import Flashcard, SessionStats
from quiz_modes.base import QuizMode
from quiz_modes.sequential import SequentialMode
from quiz_modes.random import RandomMode
from quiz_modes.adaptive import AdaptiveMode

_EXIT_SIGNAL = "exit"

_ModeFactory = Callable[[List[Flashcard]], QuizMode]

_MODE_MAP: Dict[str, _ModeFactory] = {
    "sequential": SequentialMode,
    "random": RandomMode,
    "adaptive": AdaptiveMode,
}

SUPPORTED_MODES: List[str] = list(_MODE_MAP.keys())


def get_quiz_mode(mode: str, cards: List[Flashcard]) -> QuizMode:
    """Factory: return the correct QuizMode strategy for the given mode string.

    Args:
        mode: One of 'sequential', 'random', or 'adaptive'.
        cards: Flashcards to pass to the mode implementation.

    Returns:
        An initialised QuizMode instance.

    Raises:
        InvalidModeError: If the mode string is not recognised.
    """
    key = mode.lower()
    if key not in _MODE_MAP:
        supported = ", ".join(_MODE_MAP)
        raise InvalidModeError(
            f"Unknown quiz mode '{mode}'. Supported modes: {supported}."
        )
    return _MODE_MAP[key](cards)


@dataclasses.dataclass(frozen=True)
class AnswerResult:
    """Immutable result of a single answered card."""

    card: Flashcard
    given: str
    correct: bool


def _answers_match(given: str, expected: str) -> bool:
    """Return True if *given* matches *expected* case-insensitively after stripping.

    Args:
        given: The user's raw answer string.
        expected: The card's back text.

    Returns:
        True when the normalised strings are equal.
    """
    return given.strip().lower() == expected.strip().lower()


def run_session(
    mode: QuizMode,
    input_fn: Callable[[Flashcard], Optional[str]],
) -> Iterator[Tuple[AnswerResult, SessionStats]]:
    """Drive the quiz session and yield results one card at a time.

    The function is decoupled from argparse, colorama, and ``input()``.
    The caller supplies *input_fn*, which receives the current card and
    returns the user's answer string, or ``None`` / the sentinel ``"exit"``
    to stop the session early.

    Args:
        mode: An initialised QuizMode strategy (sequential, random, adaptive).
        input_fn: Callable that accepts a Flashcard and returns the user's
            answer string, or None to signal session termination.

    Yields:
        A ``(AnswerResult, SessionStats)`` tuple after every answered card.
        The yielded ``SessionStats`` reflects cumulative totals up to that
        point, allowing the caller to render feedback after each card.
    """
    stats = SessionStats()

    while mode.has_remaining():
        card = mode.next_card()
        if card is None:
            break

        raw = input_fn(card)

        if raw is None or raw.strip().lower() == _EXIT_SIGNAL:
            break

        correct = _answers_match(raw, card.back)
        stats.total += 1

        if correct:
            stats.correct += 1
        else:
            if card.front not in stats.missed:
                stats.missed.append(card.front)

        mode.mark_answer(card, correct=correct)
        yield AnswerResult(card=card, given=raw, correct=correct), dataclasses.replace(
            stats
        )


def display_stats(stats: SessionStats) -> None:
    """Print session statistics to stdout.

    Args:
        stats: The completed session's statistics.
    """
    print("\n--- Session Statistics ---")
    print(f"Total questions : {stats.total}")
    print(f"Correct answers : {stats.correct}")
    print(f"Accuracy        : {stats.accuracy:.1f}%")
    if stats.missed:
        print("Missed terms    :")
        for term in stats.missed:
            print(f"  - {term}")
    else:
        print("Missed terms    : none")
