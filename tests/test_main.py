"""Unit tests for main.py: build_parser, _make_input_fn, run_quiz, main."""

import argparse
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

import main  # noqa: E402
from main import _make_input_fn, build_parser, run_quiz  # noqa: E402
from models import Flashcard  # noqa: E402

# ---------------------------------------------------------------------------
# build_parser
# ---------------------------------------------------------------------------


def test_build_parser_returns_parser() -> None:
    """build_parser returns an ArgumentParser instance."""
    parser = build_parser()
    assert isinstance(parser, argparse.ArgumentParser)


def test_build_parser_file_flag() -> None:
    """-f / --file is accepted."""
    parser = build_parser()
    args = parser.parse_args(["-f", "some.json", "-m", "sequential"])
    assert args.file == "some.json"


def test_build_parser_mode_flag() -> None:
    """-m / --mode is accepted and defaults to sequential."""
    parser = build_parser()
    args = parser.parse_args(["-f", "x.json"])
    assert args.mode == "sequential"
    args2 = parser.parse_args(["-f", "x.json", "-m", "random"])
    assert args2.mode == "random"


def test_build_parser_stats_flag() -> None:
    """--stats defaults to False; True when supplied."""
    parser = build_parser()
    args = parser.parse_args(["-f", "x.json"])
    assert args.stats is False
    args2 = parser.parse_args(["-f", "x.json", "--stats"])
    assert args2.stats is True


def test_build_parser_invalid_mode_rejected() -> None:
    """An unrecognised mode value causes argparse to exit."""
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["-f", "x.json", "-m", "turbo"])


# ---------------------------------------------------------------------------
# _make_input_fn
# ---------------------------------------------------------------------------


def test_make_input_fn_returns_callable() -> None:
    """_make_input_fn returns a callable."""
    fn = _make_input_fn("A: ")
    assert callable(fn)


def test_make_input_fn_reads_input(monkeypatch: pytest.MonkeyPatch) -> None:
    """The returned callable reads from stdin via input()."""
    monkeypatch.setattr("builtins.input", lambda _: "test answer")
    fn = _make_input_fn("A: ")
    card = Flashcard(front="Q", back="A")
    result = fn(card)
    assert result == "test answer"


def test_make_input_fn_handles_eoferror(monkeypatch: pytest.MonkeyPatch) -> None:
    """The returned callable returns None on EOFError."""

    def _raise(_: str) -> str:
        raise EOFError

    monkeypatch.setattr("builtins.input", _raise)
    fn = _make_input_fn("A: ")
    card = Flashcard(front="Q", back="A")
    assert fn(card) is None


# ---------------------------------------------------------------------------
# run_quiz
# ---------------------------------------------------------------------------


def _make_args(
    file: str = "data/glossary.json",
    mode: str = "sequential",
    stats: bool = False,
) -> argparse.Namespace:
    return argparse.Namespace(file=file, mode=mode, stats=stats)


def test_run_quiz_exits_on_missing_file(capsys: pytest.CaptureFixture[str]) -> None:
    """run_quiz exits with code 1 and prints an error for a missing file."""
    with pytest.raises(SystemExit) as exc_info:
        run_quiz(_make_args(file="nonexistent_xyz.json"))
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error" in captured.err


def test_run_quiz_exits_on_invalid_mode(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """run_quiz exits with code 1 when get_quiz_mode raises InvalidModeError."""
    import json

    card_file = tmp_path / "cards.json"
    card_file.write_text(json.dumps([{"front": "Q", "back": "A"}]), encoding="utf-8")
    with pytest.raises(SystemExit) as exc_info:
        run_quiz(_make_args(file=str(card_file), mode="badmode"))
    assert exc_info.value.code == 1
    assert "Error" in capsys.readouterr().err


def test_run_quiz_runs_session(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """run_quiz loads cards and drives a session; exit terminates cleanly."""
    import json

    card_file = tmp_path / "cards.json"
    card_file.write_text(json.dumps([{"front": "Q1", "back": "A1"}]), encoding="utf-8")
    monkeypatch.setattr("builtins.input", lambda _: "exit")
    run_quiz(_make_args(file=str(card_file), mode="sequential"))


def test_run_quiz_displays_stats_flag(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """run_quiz calls display_stats when --stats is set."""
    import json

    card_file = tmp_path / "cards.json"
    card_file.write_text(json.dumps([{"front": "Q1", "back": "A1"}]), encoding="utf-8")
    monkeypatch.setattr("builtins.input", lambda _: "exit")
    run_quiz(_make_args(file=str(card_file), mode="sequential", stats=True))
    out = capsys.readouterr().out
    assert "Session Statistics" in out


def test_run_quiz_correct_answer_green(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A correct answer triggers 'Correct!' in the output."""
    import json

    card_file = tmp_path / "cards.json"
    card_file.write_text(json.dumps([{"front": "Q1", "back": "A1"}]), encoding="utf-8")
    answers = iter(["A1"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    run_quiz(_make_args(file=str(card_file)))
    out = capsys.readouterr().out
    assert "Correct!" in out


def test_run_quiz_incorrect_answer_red(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """An incorrect answer triggers 'Incorrect.' in the output."""
    import json

    card_file = tmp_path / "cards.json"
    card_file.write_text(json.dumps([{"front": "Q1", "back": "A1"}]), encoding="utf-8")
    answers = iter(["wrong"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    run_quiz(_make_args(file=str(card_file)))
    out = capsys.readouterr().out
    assert "Incorrect" in out


def test_run_quiz_compact_summary_shows_missed_terms(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Compact summary includes missed terms when answers are wrong."""
    import json

    card_file = tmp_path / "cards.json"
    card_file.write_text(
        json.dumps([{"front": "Capital", "back": "Paris"}]), encoding="utf-8"
    )
    answers = iter(["wrong"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    run_quiz(_make_args(file=str(card_file)))
    out = capsys.readouterr().out
    assert "Missed terms" in out
    assert "Capital" in out


# ---------------------------------------------------------------------------
# main() — KeyboardInterrupt
# ---------------------------------------------------------------------------


def test_main_keyboard_interrupt_exits_cleanly(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """main() catches KeyboardInterrupt and exits with code 0."""
    monkeypatch.setattr("main.run_quiz", MagicMock(side_effect=KeyboardInterrupt))
    monkeypatch.setattr("sys.argv", ["flashcard-quizzer", "-f", "data/glossary.json"])
    with pytest.raises(SystemExit) as exc_info:
        main.main()
    assert exc_info.value.code == 0
    out = capsys.readouterr().out
    assert "Goodbye" in out
