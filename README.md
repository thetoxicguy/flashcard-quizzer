# Flashcard Quizzer

A command-line flashcard quiz application written in Python. Load flashcards from a JSON file and test yourself in sequential, random, or adaptive mode.

---

## Features

- Three quiz modes: sequential, random, and adaptive (re-queues missed cards until mastered)
- Two JSON input formats: plain array and object-wrapper
- Case-insensitive answer matching with leading/trailing whitespace ignored
- Colour-coded feedback (green = correct, red = incorrect) via colorama
- Always-on compact session summary; optional detailed statistics with `--stats`
- Graceful exit via the `exit` command or `Ctrl+C` at any prompt
- 89 tests, 99% coverage; all quality gates (black, mypy, flake8) pass

---

## Folder Structure

```
flashcard-quizzer/
├── main.py                  CLI entry point (argparse, colorama)
├── quiz_engine.py           Factory (get_quiz_mode), SUPPORTED_MODES, run_session(), display_stats()
├── models.py                Flashcard and SessionStats dataclasses
├── exceptions.py            FlashcardError, FileLoadError, ValidationError, InvalidModeError
├── requirements.txt         Runtime and development dependencies
├── setup.cfg                pytest and coverage configuration
├── mypy.ini                 mypy strict-mode configuration
├── .flake8                  flake8 configuration (max-line-length = 88)
├── .env                     Local environment overrides (not committed)
├── .gitignore
├── prompts.md               Record of AI development prompts
├── data/
│   ├── glossary.json        Sample deck — array format
│   └── python_basics.json   Sample deck — object-wrapper format
├── quiz_modes/
│   ├── base.py              QuizMode abstract base class (Strategy interface)
│   ├── sequential.py        SequentialMode
│   ├── random.py            RandomMode
│   └── adaptive.py          AdaptiveMode
├── utils/
│   └── file_handler.py      JSON loader and validator
├── tests/
│   ├── test_flashcard_loader.py
│   ├── test_quiz_modes.py
│   ├── test_quiz_engine.py
│   ├── test_main.py
│   └── test_integration.py
└── docs/
    └── ai_edit_log.md       AI-assisted development correction log
```

---

## Requirements

- Python 3.10 or later
- Dependencies listed in `requirements.txt`:

| Package | Purpose |
|---------|---------|
| `colorama` | Cross-platform terminal colours |
| `python-dotenv` | Load `.env` into the environment |
| `pytest` | Test runner |
| `pytest-cov` | Coverage plugin for pytest |
| `black` | Code formatter |
| `mypy` | Static type checker |
| `flake8` | Style linter |
| `types-colorama` | Type stubs for colorama |

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Copy or create a `.env` file in the project root for local overrides:

```
# .env — local environment configuration
# Do NOT store secrets here; use a secrets manager or OS environment variables.
# APP_ENV=development
```

The file is loaded automatically at startup via `python-dotenv`. The application does not currently require any environment variables to run; the file is provided as a structured extension point.

---

## Supported JSON Formats

### Array format

Each element is a card object with `front` (question) and `back` (answer) string fields.

```json
[
  {"front": "Algorithm", "back": "A step-by-step procedure for solving a problem"},
  {"front": "Recursion", "back": "A function that calls itself to solve a smaller subproblem"}
]
```

See `data/glossary.json` for a full example.

### Object-wrapper format

The root object must contain a `"cards"` key whose value is a card array.

```json
{
  "cards": [
    {"front": "list", "back": "An ordered, mutable sequence type in Python"},
    {"front": "dict", "back": "A mutable mapping of key-value pairs in Python"}
  ]
}
```

See `data/python_basics.json` for a full example.

**Validation rules applied to every card:**

- Both `front` and `back` must be present.
- Both fields must be non-empty strings (whitespace-only values are rejected).
- Values are stripped of leading/trailing whitespace when loaded.

---

## CLI Flags

```
usage: flashcard-quizzer [-h] -f FILE [-m MODE] [--stats]

Quiz yourself with flashcards from a JSON file.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to the JSON flashcard file.
  -m MODE, --mode MODE  Quiz mode: sequential, random, adaptive. (default: sequential)
  --stats               Display session statistics at the end.
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `-f` / `--file` | Yes | — | Path to the JSON flashcard file |
| `-m` / `--mode` | No | `sequential` | Quiz mode: `sequential`, `random`, or `adaptive` |
| `--stats` | No | off | Print detailed session statistics after the session ends |

---

## Running the Application

```bash
python main.py --help
python main.py --mode sequential --file data/glossary.json
python main.py -m adaptive -f data/python_basics.json
python main.py -f data/glossary.json -m random --stats
```

**Example session:**

```
Starting sequential quiz with 5 card(s). Type 'exit' to quit.

Q: Algorithm
A: a step-by-step procedure for solving a problem
Correct!

Q: Recursion
A: wrong answer
Incorrect. The answer is: A function that calls itself to solve a smaller subproblem

Session complete — 1/2 correct (50.0% accuracy). Missed terms: Recursion
```

---

## Quiz Modes

### `sequential`

Presents cards one by one in the exact order they appear in the JSON file. Each card is shown once. The session ends when all cards have been answered or the user exits.

### `random`

Presents all cards in a randomly shuffled order. Each card is shown once. The shuffle is performed at startup using a local RNG instance (does not affect the global random state).

### `adaptive`

Presents cards from a queue. Correctly answered cards are removed. Incorrectly answered cards are re-appended to the end of the queue and presented again later. The session ends only when every card has been answered correctly at least once, or when the user exits.

---

## Session Statistics

A compact one-line summary is **always printed** at the end of every session:

```
Session complete — X/Y correct (Z% accuracy). Missed terms: term1, term2
```

Pass `--stats` to also print the detailed breakdown:

```
--- Session Statistics ---
Total questions : 5
Correct answers : 4
Accuracy        : 80.0%
Missed terms    :
  - Recursion
```

If the session is exited early (via `exit` or `Ctrl+C`), the summary reflects only the cards answered up to that point.

---

## Graceful Exit Behavior

| Signal | Behaviour |
|--------|-----------|
| Type `exit` at any answer prompt | Session ends; compact summary is printed |
| `Ctrl+C` | Session ends with "Quiz interrupted. Goodbye!" — no partial summary |
| `EOF` (e.g. piped input exhausted) | Treated identically to `exit` |

---

## Running Tests

```bash
python -m pytest tests/
```

**Verified output (89 tests):**

```
89 passed in 0.78s
```

Test files and their scope:

| File | Tests | Scope |
|------|-------|-------|
| `tests/test_flashcard_loader.py` | 19 | JSON loading, both formats, all validation error paths |
| `tests/test_quiz_modes.py` | 19 | Factory, SequentialMode, RandomMode (seeded), AdaptiveMode |
| `tests/test_quiz_engine.py` | 21 | `_answers_match`, `run_session`, `AnswerResult`, `display_stats` |
| `tests/test_main.py` | 16 | `build_parser`, `_make_input_fn`, `run_quiz`, `main()` |
| `tests/test_integration.py` | 14 | Full session scenarios + CLI subprocess tests |

---

## Generating the Coverage Report

```bash
python -m pytest --cov=. --cov-report=html
```

Open `htmlcov/index.html` in a browser to view the line-by-line report.

**Current coverage: 99%** (235 statements, 2 missed — the `if __name__ == "__main__"` guard in `main.py` and one display branch in `display_stats`).

Coverage is configured in `setup.cfg`:

```ini
[coverage:run]
source = .
omit = tests/*, htmlcov/*, setup.cfg

[coverage:report]
omit = tests/*, htmlcov/*, setup.cfg
```

---

## Formatting, Type Checking, and Linting

All three quality gates must pass before committing.

### Formatter — black

```bash
python -m black --check .
```

Configuration: line length 88 (default). Applied automatically with `python -m black .`.

### Type checker — mypy

```bash
python -m mypy .
```

Configuration (`mypy.ini`): `strict = True`, `python_version = 3.10`, `ignore_missing_imports = True`.

### Linter — flake8

```bash
python -m flake8 .
```

Configuration (`.flake8`): `max-line-length = 88`, `extend-ignore = E203, W503`.

**Verified:** All three commands exit with code 0 on the current codebase.

---

## Architecture and Design Patterns

### Strategy pattern

`QuizMode` (`quiz_modes/base.py`) is an abstract base class defining three abstract methods:

- `next_card() -> Optional[Flashcard]` — return the next card to present
- `mark_answer(card, correct)` — record the result of an answered card
- `has_remaining() -> bool` — indicate whether cards remain

Three concrete strategies implement the interface:

| Class | Module | Behaviour |
|-------|--------|-----------|
| `SequentialMode` | `quiz_modes/sequential.py` | Original file order, each card once |
| `RandomMode` | `quiz_modes/random.py` | Shuffled order, each card once |
| `AdaptiveMode` | `quiz_modes/adaptive.py` | Queue-based; incorrect cards re-queued |

### Factory pattern

`get_quiz_mode(mode: str, cards: List[Flashcard]) -> QuizMode` in `quiz_engine.py` maps the CLI `--mode` string to a strategy instance via `_MODE_MAP`. `SUPPORTED_MODES` is derived directly from `_MODE_MAP.keys()` and imported by `main.py` — a single source of truth that argparse `choices` and help text both reference.

### Dependency injection in the session engine

`run_session(mode, input_fn)` is a generator that accepts any callable matching `Callable[[Flashcard], Optional[str]]` as its I/O interface. This decouples the engine from `input()`, `colorama`, and `argparse`, enabling straightforward unit testing with scripted answer sequences without monkey-patching.

---

## AI Interaction Log

All AI-assisted development corrections, prompt improvements, and defect fixes are recorded in [`docs/ai_edit_log.md`](docs/ai_edit_log.md). The log currently contains 19 entries covering:

- Design decisions (module layout, Strategy/Factory patterns)
- Defects fixed during implementation (validation gaps, mypy errors, flake8 conflicts)
- Testability improvements (seeded RNG in RandomMode, injectable `input_fn`)
- Refactors applied from engineering review (frozen dataclass, snapshot yield, annotation widening)
