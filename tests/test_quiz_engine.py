"""Tests for quiz_engine: run_session, AnswerResult, _answers_match, display_stats."""

import sys
from pathlib import Path
from typing import Callable, Iterator, List, Optional, Sequence, Tuple

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from models import Flashcard, SessionStats  # noqa: E402
from quiz_engine import (  # noqa: E402
    AnswerResult,
    _answers_match,
    display_stats,
    run_session,
)
from quiz_modes.adaptive import AdaptiveMode  # noqa: E402
from quiz_modes.sequential import SequentialMode  # noqa: E402

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_cards(*pairs: Tuple[str, str]) -> List[Flashcard]:
    """Build a list of Flashcard objects from (front, back) pairs."""
    return [Flashcard(front=f, back=b) for f, b in pairs]


def scripted_input(answers: List[Optional[str]]) -> Iterator[Optional[str]]:
    """Yield each answer in order; used as a side-effect source for input_fn."""
    return iter(answers)


def input_fn_from(
    answers: Sequence[Optional[str]],
) -> Callable[[Flashcard], Optional[str]]:
    """Return a callable that pops answers in order, ignoring the card argument."""
    it = iter(answers)

    def _fn(card: Flashcard) -> Optional[str]:
        return next(it, None)

    return _fn


# ---------------------------------------------------------------------------
# _answers_match tests
# ---------------------------------------------------------------------------


def test_answers_match_exact() -> None:
    """Exact match returns True."""
    assert _answers_match("Python", "Python")


def test_answers_match_case_insensitive() -> None:
    """Case-insensitive correct answer returns True."""
    assert _answers_match("PYTHON", "python")
    assert _answers_match("python", "PYTHON")
    assert _answers_match("PyThOn", "python")


def test_answers_match_strips_whitespace() -> None:
    """Leading/trailing whitespace is ignored."""
    assert _answers_match("  python  ", "python")
    assert _answers_match("python", "  python  ")


def test_answers_match_wrong_answer() -> None:
    """A wrong answer returns False."""
    assert not _answers_match("Java", "Python")


def test_answers_match_empty_vs_nonempty() -> None:
    """An empty answer does not match a non-empty expected value."""
    assert not _answers_match("", "Python")


# ---------------------------------------------------------------------------
# run_session — correctness and stats
# ---------------------------------------------------------------------------


def test_run_session_correct_answer_updates_stats() -> None:
    """A correct answer increments total and correct counts."""
    cards = make_cards(("Capital of France", "Paris"))
    mode = SequentialMode(cards)
    results = list(run_session(mode, input_fn_from(["Paris"])))
    assert len(results) == 1
    result, stats = results[0]
    assert result.correct is True
    assert stats.total == 1
    assert stats.correct == 1
    assert stats.missed == []


def test_run_session_case_insensitive_correct_answer() -> None:
    """Case-insensitive correct answer is marked correct."""
    cards = make_cards(("Capital of France", "Paris"))
    mode = SequentialMode(cards)
    results = list(run_session(mode, input_fn_from(["PARIS"])))
    result, stats = results[0]
    assert result.correct is True
    assert stats.correct == 1


def test_run_session_incorrect_answer_captured_in_missed() -> None:
    """Incorrect answer is captured in missed terms."""
    cards = make_cards(("Capital of France", "Paris"))
    mode = SequentialMode(cards)
    results = list(run_session(mode, input_fn_from(["London"])))
    result, stats = results[0]
    assert result.correct is False
    assert "Capital of France" in stats.missed


def test_run_session_accuracy_calculated_correctly() -> None:
    """Accuracy is calculated correctly across mixed answers."""
    cards = make_cards(("Q1", "A1"), ("Q2", "A2"), ("Q3", "A3"), ("Q4", "A4"))
    mode = SequentialMode(cards)
    answers = ["A1", "wrong", "A3", "wrong"]
    all_results = list(run_session(mode, input_fn_from(answers)))
    _, stats = all_results[-1]
    assert stats.total == 4
    assert stats.correct == 2
    assert stats.accuracy == pytest.approx(50.0)


def test_run_session_full_correct_accuracy() -> None:
    """100% accuracy when all answers are correct."""
    cards = make_cards(("Q1", "A1"), ("Q2", "A2"))
    mode = SequentialMode(cards)
    all_results = list(run_session(mode, input_fn_from(["A1", "A2"])))
    _, stats = all_results[-1]
    assert stats.accuracy == pytest.approx(100.0)


def test_run_session_empty_session_safe_stats() -> None:
    """An empty session (no cards) returns no results and safe zero stats."""
    mode = SequentialMode([])
    results = list(run_session(mode, input_fn_from([])))
    assert results == []


def test_run_session_interrupted_by_none_returns_safe_stats() -> None:
    """Interrupted session (input_fn returns None) terminates without error."""
    cards = make_cards(("Q1", "A1"), ("Q2", "A2"))
    mode = SequentialMode(cards)
    results = list(run_session(mode, input_fn_from([None])))
    assert results == []


def test_run_session_interrupted_by_exit_signal() -> None:
    """User typing 'exit' terminates the session cleanly."""
    cards = make_cards(("Q1", "A1"), ("Q2", "A2"))
    mode = SequentialMode(cards)
    results = list(run_session(mode, input_fn_from(["exit"])))
    assert results == []


def test_run_session_exit_after_first_answer() -> None:
    """Session stops after 'exit' even with remaining cards."""
    cards = make_cards(("Q1", "A1"), ("Q2", "A2"), ("Q3", "A3"))
    mode = SequentialMode(cards)
    results = list(run_session(mode, input_fn_from(["A1", "exit"])))
    assert len(results) == 1
    _, stats = results[0]
    assert stats.total == 1


def test_run_session_missed_term_not_duplicated() -> None:
    """A term answered incorrectly multiple times appears in missed only once."""
    card = Flashcard(front="Q1", back="A1")
    mode = AdaptiveMode([card])
    answers = ["wrong1", "wrong2", "A1"]
    results = list(run_session(mode, input_fn_from(answers)))
    _, final_stats = results[-1]
    assert final_stats.missed.count("Q1") == 1


# ---------------------------------------------------------------------------
# AdaptiveMode integration via run_session
# ---------------------------------------------------------------------------


def test_adaptive_mode_revisits_incorrect_card() -> None:
    """Adaptive mode re-presents a card answered incorrectly."""
    cards = make_cards(("Q1", "A1"))
    mode = AdaptiveMode(cards)
    answers = ["wrong", "A1"]
    results = list(run_session(mode, input_fn_from(answers)))
    assert len(results) == 2
    assert results[0][0].correct is False
    assert results[1][0].correct is True
    _, final_stats = results[-1]
    assert final_stats.total == 2
    assert final_stats.correct == 1


def test_adaptive_mode_terminates_after_all_correct() -> None:
    """Adaptive session ends once every card is answered correctly."""
    cards = make_cards(("Q1", "A1"), ("Q2", "A2"))
    mode = AdaptiveMode(cards)
    answers = ["wrong", "A2", "A1"]
    results = list(run_session(mode, input_fn_from(answers)))
    fronts = [r.card.front for r, _ in results]
    assert fronts == ["Q1", "Q2", "Q1"]
    _, stats = results[-1]
    assert stats.total == 3
    assert stats.correct == 2


# ---------------------------------------------------------------------------
# display_stats — output smoke test
# ---------------------------------------------------------------------------


def test_display_stats_no_missed(capsys: pytest.CaptureFixture[str]) -> None:
    """display_stats prints correct output when no terms are missed."""
    stats = SessionStats(total=3, correct=3, missed=[])
    display_stats(stats)
    out = capsys.readouterr().out
    assert "100.0%" in out
    assert "none" in out


def test_display_stats_with_missed(capsys: pytest.CaptureFixture[str]) -> None:
    """display_stats lists missed terms."""
    stats = SessionStats(total=2, correct=1, missed=["Term X"])
    display_stats(stats)
    out = capsys.readouterr().out
    assert "Term X" in out
    assert "50.0%" in out


def test_display_stats_zero_total(capsys: pytest.CaptureFixture[str]) -> None:
    """display_stats handles a zero-total session without division-by-zero."""
    stats = SessionStats()
    display_stats(stats)
    out = capsys.readouterr().out
    assert "0.0%" in out


# ---------------------------------------------------------------------------
# AnswerResult
# ---------------------------------------------------------------------------


def test_answer_result_stores_fields() -> None:
    """AnswerResult correctly stores card, given answer, and correctness."""
    card = Flashcard(front="Q", back="A")
    result = AnswerResult(card=card, given="a", correct=True)
    assert result.card is card
    assert result.given == "a"
    assert result.correct is True
