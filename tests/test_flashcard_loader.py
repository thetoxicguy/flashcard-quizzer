"""Tests for utils/file_handler.py — flashcard loading and validation."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from exceptions import FileLoadError, ValidationError  # noqa: E402
from utils.file_handler import load_flashcards  # noqa: E402

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def write_json(tmp_path: Path, data: object, filename: str = "cards.json") -> str:
    """Write *data* as JSON to *tmp_path/filename* and return the path string."""
    file = tmp_path / filename
    file.write_text(json.dumps(data), encoding="utf-8")
    return str(file)


# ---------------------------------------------------------------------------
# Happy-path tests
# ---------------------------------------------------------------------------


def test_load_valid_flashcards_array(tmp_path: Path) -> None:
    """Array-format JSON is loaded and returned as a list of Flashcard objects."""
    data = [{"front": "Term A", "back": "Definition A"}]
    path = write_json(tmp_path, data)
    cards = load_flashcards(path)
    assert len(cards) == 1
    assert cards[0].front == "Term A"
    assert cards[0].back == "Definition A"


def test_load_valid_flashcards_object_wrapper(tmp_path: Path) -> None:
    """Object-wrapper format JSON is accepted and returns correct Flashcard list."""
    data = {"cards": [{"front": "Q1", "back": "A1"}, {"front": "Q2", "back": "A2"}]}
    path = write_json(tmp_path, data)
    cards = load_flashcards(path)
    assert len(cards) == 2
    assert cards[1].front == "Q2"


def test_load_multiple_cards_array(tmp_path: Path) -> None:
    """All cards in an array file are loaded without loss."""
    data = [{"front": f"Q{i}", "back": f"A{i}"} for i in range(5)]
    path = write_json(tmp_path, data)
    cards = load_flashcards(path)
    assert len(cards) == 5


# ---------------------------------------------------------------------------
# Error-path tests
# ---------------------------------------------------------------------------


def test_load_missing_file() -> None:
    """A non-existent file path raises FileLoadError with a helpful message."""
    with pytest.raises(FileLoadError, match="not found"):
        load_flashcards("/tmp/this_file_does_not_exist_xyz.json")


def test_load_invalid_json(tmp_path: Path) -> None:
    """A file containing invalid JSON raises FileLoadError."""
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{not valid json", encoding="utf-8")
    with pytest.raises(FileLoadError, match="Invalid JSON"):
        load_flashcards(str(bad_file))


def test_load_missing_required_field_front(tmp_path: Path) -> None:
    """A card missing 'front' raises ValidationError."""
    data = [{"back": "Definition only"}]
    path = write_json(tmp_path, data)
    with pytest.raises(ValidationError, match="front"):
        load_flashcards(path)


def test_load_missing_required_field_back(tmp_path: Path) -> None:
    """A card missing 'back' raises ValidationError."""
    data = [{"front": "Term only"}]
    path = write_json(tmp_path, data)
    with pytest.raises(ValidationError, match="back"):
        load_flashcards(path)


def test_load_missing_required_field(tmp_path: Path) -> None:
    """A card missing both required fields raises ValidationError."""
    data = [{"question": "irrelevant"}]
    path = write_json(tmp_path, data)
    with pytest.raises(ValidationError):
        load_flashcards(path)


def test_reject_empty_string_front(tmp_path: Path) -> None:
    """A card with an empty 'front' string raises ValidationError."""
    data = [{"front": "  ", "back": "Answer"}]
    path = write_json(tmp_path, data)
    with pytest.raises(ValidationError, match="non-empty"):
        load_flashcards(path)


def test_reject_empty_string_back(tmp_path: Path) -> None:
    """A card with an empty 'back' string raises ValidationError."""
    data = [{"front": "Question", "back": ""}]
    path = write_json(tmp_path, data)
    with pytest.raises(ValidationError, match="non-empty"):
        load_flashcards(path)


def test_reject_empty_or_non_string_fields(tmp_path: Path) -> None:
    """Non-string field values raise ValidationError."""
    data = [{"front": 42, "back": None}]
    path = write_json(tmp_path, data)
    with pytest.raises(ValidationError, match="non-empty string"):
        load_flashcards(path)


def test_reject_non_object_card(tmp_path: Path) -> None:
    """A card that is not a dict (e.g. a string) raises ValidationError."""
    data = ["not a card"]
    path = write_json(tmp_path, data)
    with pytest.raises(ValidationError, match="must be an object"):
        load_flashcards(path)


def test_reject_empty_cards_list(tmp_path: Path) -> None:
    """An empty cards list raises ValidationError."""
    data: list[object] = []
    path = write_json(tmp_path, data)
    with pytest.raises(ValidationError, match="No cards found"):
        load_flashcards(path)


def test_reject_object_without_cards_key(tmp_path: Path) -> None:
    """An object-format file missing the 'cards' key raises ValidationError."""
    data = {"flashcards": [{"front": "Q", "back": "A"}]}
    path = write_json(tmp_path, data)
    with pytest.raises(ValidationError, match="'cards' key"):
        load_flashcards(path)


def test_reject_unsupported_root_type(tmp_path: Path) -> None:
    """A JSON file whose root is a number or string raises ValidationError."""
    path = write_json(tmp_path, 42)
    with pytest.raises(ValidationError, match="Unsupported JSON structure"):
        load_flashcards(path)


def test_whitespace_stripped_from_fields(tmp_path: Path) -> None:
    """Leading/trailing whitespace in front/back is stripped."""
    data = [{"front": "  Term  ", "back": "  Def  "}]
    path = write_json(tmp_path, data)
    cards = load_flashcards(path)
    assert cards[0].front == "Term"
    assert cards[0].back == "Def"


def test_reject_cards_value_not_a_list(tmp_path: Path) -> None:
    """An object where 'cards' is not a list raises ValidationError."""
    data = {"cards": "not a list"}
    path = write_json(tmp_path, data)
    with pytest.raises(ValidationError, match="must be a list"):
        load_flashcards(path)


def test_load_path_is_directory_raises_file_load_error(tmp_path: Path) -> None:
    """Passing a directory path raises FileLoadError."""
    with pytest.raises(FileLoadError, match="not a file"):
        load_flashcards(str(tmp_path))


def test_load_oserror_on_read(tmp_path: Path) -> None:
    """An OSError during file read raises FileLoadError."""
    from unittest.mock import patch

    card_file = tmp_path / "cards.json"
    card_file.write_text('[{"front": "Q", "back": "A"}]', encoding="utf-8")

    with patch("utils.file_handler.Path.read_text", side_effect=OSError("disk error")):
        with pytest.raises(FileLoadError, match="Cannot read file"):
            load_flashcards(str(card_file))
