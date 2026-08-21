# Flashcard Quizzer

A command-line flashcard quiz application written in Python.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py --help
python main.py -f data/glossary.json -m sequential
python main.py -f data/python_basics.json -m adaptive --stats
python main.py -f data/glossary.json -m random --stats
```

### CLI Flags

| Flag | Description |
|------|-------------|
| `-f / --file` | Path to the JSON flashcard file (required) |
| `-m / --mode` | Quiz mode: `sequential`, `random`, or `adaptive` (default: sequential) |
| `--stats` | Display session statistics at the end |

Type `exit` at any answer prompt to quit. Press `Ctrl+C` to quit at any time.

## JSON Formats

**Array format** (`data/glossary.json`):
```json
[
  {"front": "Term", "back": "Definition"}
]
```

**Object-wrapper format** (`data/python_basics.json`):
```json
{
  "cards": [
    {"front": "Term", "back": "Definition"}
  ]
}
```

## Architecture

```
main.py              — CLI entry point (argparse)
quiz_engine.py       — Factory (get_quiz_mode) + SUPPORTED_MODES + session engine + stats
models.py            — Flashcard and SessionStats dataclasses
exceptions.py        — Custom application exceptions
utils/
  file_handler.py    — JSON loader and validator
quiz_modes/
  base.py            — QuizMode abstract base class (Strategy interface)
  sequential.py      — SequentialMode
  random.py          — RandomMode
  adaptive.py        — AdaptiveMode
data/                — Sample JSON flashcard files
tests/               — Pytest test suite (89 tests, 99% coverage)
docs/                — AI edit log and documentation
setup.cfg            — pytest and coverage configuration
```

### Design Patterns

- **Strategy**: `QuizMode` ABC with `SequentialMode`, `RandomMode`, `AdaptiveMode`
- **Factory**: `get_quiz_mode()` in `quiz_engine.py` selects implementation from CLI value

## Testing

```bash
python -m pytest tests/ -v
python -m pytest --cov=. --cov-report=html
```

Current coverage: **99%** (237 statements, 2 missed — `__main__` guard and one display branch).

## Quality Gates

```bash
black --check .
mypy .
flake8 .
```
