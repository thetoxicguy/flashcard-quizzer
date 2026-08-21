"""Tests for Strategy pattern quiz modes and the Factory function."""

import sys
from pathlib import Path
from typing import List

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from exceptions import InvalidModeError  # noqa: E402
from models import Flashcard  # noqa: E402
from quiz_engine import get_quiz_mode  # noqa: E402
from quiz_modes.adaptive import AdaptiveMode  # noqa: E402
from quiz_modes.random import RandomMode  # noqa: E402
from quiz_modes.sequential import SequentialMode  # noqa: E402

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def three_cards() -> List[Flashcard]:
    """Return a deterministic list of three flashcards."""
    return [
        Flashcard(front="A", back="1"),
        Flashcard(front="B", back="2"),
        Flashcard(front="C", back="3"),
    ]


# ---------------------------------------------------------------------------
# Factory tests
# ---------------------------------------------------------------------------


def test_quiz_mode_factory_sequential(three_cards: List[Flashcard]) -> None:
    """Factory returns a SequentialMode for 'sequential' input."""
    mode = get_quiz_mode("sequential", three_cards)
    assert isinstance(mode, SequentialMode)


def test_quiz_mode_factory_random(three_cards: List[Flashcard]) -> None:
    """Factory returns a RandomMode for 'random' input."""
    mode = get_quiz_mode("random", three_cards)
    assert isinstance(mode, RandomMode)


def test_quiz_mode_factory_adaptive(three_cards: List[Flashcard]) -> None:
    """Factory returns an AdaptiveMode for 'adaptive' input."""
    mode = get_quiz_mode("adaptive", three_cards)
    assert isinstance(mode, AdaptiveMode)


def test_quiz_mode_factory(three_cards: List[Flashcard]) -> None:
    """Factory correctly maps all three supported mode strings."""
    for name, expected_type in [
        ("sequential", SequentialMode),
        ("random", RandomMode),
        ("adaptive", AdaptiveMode),
    ]:
        assert isinstance(get_quiz_mode(name, three_cards), expected_type)


def test_factory_rejects_invalid_mode(three_cards: List[Flashcard]) -> None:
    """Factory raises InvalidModeError for an unrecognised mode string."""
    with pytest.raises(InvalidModeError, match="Unknown quiz mode"):
        get_quiz_mode("turbo", three_cards)


def test_factory_rejects_empty_mode(three_cards: List[Flashcard]) -> None:
    """Factory raises InvalidModeError for an empty mode string."""
    with pytest.raises(InvalidModeError):
        get_quiz_mode("", three_cards)


def test_factory_mode_matching_is_case_insensitive(
    three_cards: List[Flashcard],
) -> None:
    """Factory accepts mode strings regardless of case."""
    assert isinstance(get_quiz_mode("SEQUENTIAL", three_cards), SequentialMode)
    assert isinstance(get_quiz_mode("Random", three_cards), RandomMode)
    assert isinstance(get_quiz_mode("ADAPTIVE", three_cards), AdaptiveMode)


# ---------------------------------------------------------------------------
# SequentialMode tests
# ---------------------------------------------------------------------------


def test_sequential_mode_order(three_cards: List[Flashcard]) -> None:
    """SequentialMode returns cards in the exact original order."""
    mode = SequentialMode(three_cards)
    results = []
    while mode.has_remaining():
        card = mode.next_card()
        assert card is not None
        results.append(card.front)
    assert results == ["A", "B", "C"]


def test_sequential_mode_exhausted_returns_none(three_cards: List[Flashcard]) -> None:
    """SequentialMode returns None after all cards are exhausted."""
    mode = SequentialMode(three_cards)
    for _ in range(3):
        mode.next_card()
    assert mode.next_card() is None
    assert not mode.has_remaining()


def test_sequential_mode_does_not_mutate_input(three_cards: List[Flashcard]) -> None:
    """SequentialMode does not mutate the caller's original list."""
    original = list(three_cards)
    SequentialMode(three_cards)
    assert three_cards == original


def test_sequential_mode_mark_answer_is_noop(three_cards: List[Flashcard]) -> None:
    """SequentialMode.mark_answer does not affect card order or count."""
    mode = SequentialMode(three_cards)
    card = mode.next_card()
    assert card is not None
    mode.mark_answer(card, correct=False)
    assert mode.has_remaining()
    assert mode.next_card() is not None


# ---------------------------------------------------------------------------
# RandomMode tests
# ---------------------------------------------------------------------------


def test_random_mode_preserves_cards(three_cards: List[Flashcard]) -> None:
    """RandomMode delivers the same set of cards as the input, just reordered."""
    mode = RandomMode(three_cards, seed=42)
    delivered = []
    while mode.has_remaining():
        card = mode.next_card()
        assert card is not None
        delivered.append(card)
    assert len(delivered) == len(three_cards)
    assert set(c.front for c in delivered) == set(c.front for c in three_cards)


def test_random_mode_does_not_mutate_input(three_cards: List[Flashcard]) -> None:
    """RandomMode does not mutate the caller's original list."""
    original = list(three_cards)
    RandomMode(three_cards, seed=0)
    assert three_cards == original


def test_random_mode_shuffles_with_seed(three_cards: List[Flashcard]) -> None:
    """Two RandomMode instances with the same seed produce the same order."""
    mode_a = RandomMode(three_cards, seed=99)
    mode_b = RandomMode(three_cards, seed=99)
    order_a = [mode_a.next_card() for _ in range(3)]
    order_b = [mode_b.next_card() for _ in range(3)]
    assert order_a == order_b


def test_random_mode_exhausted_returns_none(three_cards: List[Flashcard]) -> None:
    """RandomMode returns None after all cards have been delivered."""
    mode = RandomMode(three_cards, seed=1)
    for _ in range(3):
        mode.next_card()
    assert mode.next_card() is None
    assert not mode.has_remaining()


# ---------------------------------------------------------------------------
# AdaptiveMode tests
# ---------------------------------------------------------------------------


def test_adaptive_mode_behavior(three_cards: List[Flashcard]) -> None:
    """AdaptiveMode re-queues incorrectly answered cards and eventually terminates."""
    mode = AdaptiveMode(three_cards)
    answered: List[str] = []
    seen: set[str] = set()

    while mode.has_remaining():
        card = mode.next_card()
        assert card is not None
        correct = card.front not in seen
        seen.add(card.front)
        mode.mark_answer(card, correct=correct)
        answered.append(card.front)

    assert set(answered) == {"A", "B", "C"}


def test_adaptive_mode_correct_answer_removes_card(
    three_cards: List[Flashcard],
) -> None:
    """A correctly answered card is not re-queued."""
    mode = AdaptiveMode([three_cards[0]])
    card = mode.next_card()
    assert card is not None
    mode.mark_answer(card, correct=True)
    assert not mode.has_remaining()


def test_adaptive_mode_incorrect_answer_requeues_card(
    three_cards: List[Flashcard],
) -> None:
    """An incorrectly answered card is appended back to the queue."""
    mode = AdaptiveMode([three_cards[0]])
    card = mode.next_card()
    assert card is not None
    mode.mark_answer(card, correct=False)
    assert mode.has_remaining()
    requeued = mode.next_card()
    assert requeued == card


def test_adaptive_mode_exhausted_returns_none(three_cards: List[Flashcard]) -> None:
    """AdaptiveMode returns None when the queue is empty."""
    mode = AdaptiveMode([three_cards[0]])
    card = mode.next_card()
    assert card is not None
    mode.mark_answer(card, correct=True)
    assert mode.next_card() is None
