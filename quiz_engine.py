"""Quiz engine: factory, session orchestration, and statistics display."""

from typing import Callable, Dict, List

from exceptions import InvalidModeError
from models import Flashcard, SessionStats
from quiz_modes.base import QuizMode
from quiz_modes.sequential import SequentialMode
from quiz_modes.random import RandomMode
from quiz_modes.adaptive import AdaptiveMode

_ModeFactory = Callable[[List[Flashcard]], QuizMode]

_MODE_MAP: Dict[str, _ModeFactory] = {
    "sequential": SequentialMode,
    "random": RandomMode,
    "adaptive": AdaptiveMode,
}


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
