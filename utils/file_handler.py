"""Flashcard file loader with support for array and object-wrapper JSON formats."""

import json
from pathlib import Path
from typing import Any, List

from exceptions import FileLoadError, ValidationError
from models import Flashcard


def _validate_card(raw: Any, index: int) -> Flashcard:
    """Validate a single raw card dict and return a Flashcard.

    Args:
        raw: The raw value from the JSON array.
        index: Zero-based position of the card (used in error messages).

    Returns:
        A validated Flashcard instance.

    Raises:
        ValidationError: If the card is malformed or missing required fields.
    """
    if not isinstance(raw, dict):
        raise ValidationError(
            f"Card at index {index} must be an object, got {type(raw).__name__}."
        )
    for field in ("front", "back"):
        if field not in raw:
            raise ValidationError(
                f"Card at index {index} is missing required field '{field}'."
            )
        value = raw[field]
        if not isinstance(value, str) or not value.strip():
            raise ValidationError(
                f"Card at index {index}: field '{field}' must be a non-empty string."
            )
    return Flashcard(front=raw["front"].strip(), back=raw["back"].strip())


def _extract_card_list(data: Any) -> List[Any]:
    """Extract the raw list of card dicts from either supported JSON format.

    Args:
        data: Parsed JSON root (list or dict).

    Returns:
        The raw list of card objects.

    Raises:
        ValidationError: If the root structure is unsupported or cards list is missing.
    """
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if "cards" not in data:
            raise ValidationError(
                "Object-format JSON must contain a 'cards' key at the root."
            )
        cards = data["cards"]
        if not isinstance(cards, list):
            raise ValidationError("The 'cards' value must be a list of card objects.")
        return cards
    raise ValidationError(
        "Unsupported JSON structure: root must be a list or an object with a "
        "'cards' key."
    )


def load_flashcards(file_path: str) -> List[Flashcard]:
    """Load and validate flashcards from a JSON file.

    Supports two formats:
    - Array: ``[{"front": "...", "back": "..."}, ...]``
    - Object wrapper: ``{"cards": [{"front": "...", "back": "..."}, ...]}``

    Args:
        file_path: Path to the JSON flashcard file.

    Returns:
        A list of validated Flashcard instances.

    Raises:
        FileLoadError: If the file does not exist or cannot be read/parsed.
        ValidationError: If the data structure or card fields are invalid.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileLoadError(f"File not found: '{file_path}'.")
    if not path.is_file():
        raise FileLoadError(f"Path is not a file: '{file_path}'.")

    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise FileLoadError(f"Cannot read file '{file_path}': {exc}") from exc

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise FileLoadError(
            f"Invalid JSON in '{file_path}': {exc.msg} (line {exc.lineno})."
        ) from exc

    raw_cards = _extract_card_list(data)

    if not raw_cards:
        raise ValidationError(f"No cards found in '{file_path}'.")

    return [_validate_card(card, i) for i, card in enumerate(raw_cards)]
