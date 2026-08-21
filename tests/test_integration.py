"""Integration tests: full quiz sessions and CLI argument paths."""

import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Sequence, Callable

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from models import Flashcard  # noqa: E402
from quiz_engine import run_session  # noqa: E402
from quiz_modes.sequential import SequentialMode  # noqa: E402
from quiz_modes.adaptive import AdaptiveMode  # noqa: E402

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

GLOSSARY = str(Path(__file__).parent.parent / "data" / "glossary.json")
PYTHON_BASICS = str(Path(__file__).parent.parent / "data" / "python_basics.json")


def input_fn_from(
    answers: Sequence[Optional[str]],
) -> Callable[[Flashcard], Optional[str]]:
    """Return a callable that delivers scripted answers in order."""
    it = iter(answers)

    def _fn(card: Flashcard) -> Optional[str]:
        return next(it, None)

    return _fn


def run_cli(*args: str, stdin: str = "") -> subprocess.CompletedProcess:  # type: ignore[type-arg]  # noqa: E501
    """Run main.py as a subprocess and return the completed process."""
    return subprocess.run(
        [sys.executable, str(Path(__file__).parent.parent / "main.py"), *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# test_full_session — three questions, mixed answers
# ---------------------------------------------------------------------------


def test_full_session() -> None:
    """Simulate a user answering three questions and verify all session stats."""
    cards = [
        Flashcard(front="Q1", back="A1"),
        Flashcard(front="Q2", back="A2"),
        Flashcard(front="Q3", back="A3"),
    ]
    answers = ["A1", "WRONG", "a3"]
    mode = SequentialMode(cards)
    results = list(run_session(mode, input_fn_from(answers)))

    assert len(results) == 3

    _, final_stats = results[-1]
    assert final_stats.total == 3
    assert final_stats.correct == 2
    assert final_stats.accuracy == pytest.approx(66.67, rel=0.01)
    assert "Q2" in final_stats.missed
    assert "Q1" not in final_stats.missed
    assert "Q3" not in final_stats.missed


def test_full_session_all_correct() -> None:
    """All-correct session yields 100% accuracy and empty missed list."""
    cards = [Flashcard(front=f"Q{i}", back=f"A{i}") for i in range(5)]
    answers = [f"A{i}" for i in range(5)]
    mode = SequentialMode(cards)
    results = list(run_session(mode, input_fn_from(answers)))
    _, stats = results[-1]
    assert stats.correct == 5
    assert stats.total == 5
    assert stats.accuracy == pytest.approx(100.0)
    assert stats.missed == []


def test_full_session_all_incorrect() -> None:
    """All-incorrect session yields 0% accuracy and all terms missed."""
    cards = [Flashcard(front="Q1", back="A1"), Flashcard(front="Q2", back="A2")]
    mode = SequentialMode(cards)
    results = list(run_session(mode, input_fn_from(["wrong", "wrong"])))
    _, stats = results[-1]
    assert stats.correct == 0
    assert stats.accuracy == pytest.approx(0.0)
    assert set(stats.missed) == {"Q1", "Q2"}


def test_full_session_adaptive_revisits_missed() -> None:
    """Adaptive full session: missed card is re-presented until correct."""
    cards = [Flashcard(front="Term", back="Def")]
    mode = AdaptiveMode(cards)
    answers = ["wrong", "wrong", "Def"]
    results = list(run_session(mode, input_fn_from(answers)))
    assert len(results) == 3
    fronts = [r.card.front for r, _ in results]
    assert fronts.count("Term") == 3
    _, stats = results[-1]
    assert stats.total == 3
    assert stats.correct == 1
    assert stats.missed == ["Term"]


def test_full_session_case_insensitive() -> None:
    """Full session accepts mixed-case answers as correct."""
    cards = [Flashcard(front="Language", back="Python")]
    mode = SequentialMode(cards)
    results = list(run_session(mode, input_fn_from(["PYTHON"])))
    result, stats = results[0]
    assert result.correct is True
    assert stats.correct == 1


def test_full_session_exit_mid_session() -> None:
    """Exiting mid-session yields partial stats without error."""
    cards = [Flashcard(front=f"Q{i}", back=f"A{i}") for i in range(4)]
    mode = SequentialMode(cards)
    answers: List[Optional[str]] = ["A0", "A1", "exit"]
    results = list(run_session(mode, input_fn_from(answers)))
    assert len(results) == 2
    _, stats = results[-1]
    assert stats.total == 2
    assert stats.correct == 2


# ---------------------------------------------------------------------------
# CLI subprocess tests
# ---------------------------------------------------------------------------


def test_cli_help_shows_all_flags() -> None:
    """--help output contains every documented flag."""
    proc = run_cli("--help")
    assert proc.returncode == 0
    for flag in ["--file", "--mode", "--stats", "-f", "-m"]:
        assert flag in proc.stdout


def test_cli_help_shows_all_modes() -> None:
    """--help output lists all three quiz modes."""
    proc = run_cli("--help")
    for mode in ["sequential", "random", "adaptive"]:
        assert mode in proc.stdout


def test_cli_sequential_glossary() -> None:
    """Sequential mode with glossary.json runs and exits cleanly."""
    proc = run_cli("-m", "sequential", "-f", GLOSSARY, stdin="exit\n")
    assert proc.returncode == 0
    assert "Starting sequential quiz" in proc.stdout


def test_cli_adaptive_python_basics() -> None:
    """Adaptive mode with python_basics.json starts without error."""
    proc = run_cli("-m", "adaptive", "-f", PYTHON_BASICS, stdin="exit\n")
    assert proc.returncode == 0
    assert "Starting adaptive quiz" in proc.stdout


def test_cli_missing_file_exits_nonzero() -> None:
    """A missing file path causes a non-zero exit and a friendly error message."""
    proc = run_cli("-f", "nonexistent.json", "-m", "sequential")
    assert proc.returncode != 0
    assert "Error" in proc.stderr or "Error" in proc.stdout


def test_cli_stats_flag_shows_detailed_output() -> None:
    """--stats flag triggers detailed session statistics output."""
    proc = run_cli("-m", "sequential", "-f", GLOSSARY, "--stats", stdin="exit\n")
    assert proc.returncode == 0
    assert "Session Statistics" in proc.stdout


def test_cli_session_summary_always_shown() -> None:
    """Compact session summary is shown even without --stats."""
    proc = run_cli("-m", "sequential", "-f", GLOSSARY, stdin="exit\n")
    assert proc.returncode == 0
    assert "Session complete" in proc.stdout


def test_cli_missing_file_flag_exits_nonzero() -> None:
    """Omitting required -f flag causes argparse to exit non-zero."""
    proc = run_cli("-m", "sequential")
    assert proc.returncode != 0
