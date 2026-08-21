# AI Edit Log

Records of prompts, corrections, improvements, and defects fixed during AI-assisted development.

---

## Entry 1 — Project Skeleton Design (Prompt 02)

**Date:** 2026-08-21
**Prompt summary:** Create project skeleton with required directories, placeholder modules, and config files.
**Correction made:** Added `quiz_modes/` package (not in original file list) to house Strategy pattern implementations cleanly, rather than embedding all three mode classes in a single `quiz_engine.py` file. This better satisfies the SOLID Single Responsibility Principle.

---

## Entry 2 — Flake8/Black Line-Length Conflict (Prompt 02)

**Date:** 2026-08-21
**Prompt summary:** Configure quality tooling.
**Defect fixed:** `black` defaults to 88-character lines while `flake8` defaults to 79. Running both without configuration would produce false-positive lint failures. Added `.flake8` with `max-line-length = 88` and `extend-ignore = E203, W503` to resolve the conflict before it caused any CI failures.

---

## Entry 3 — File Handler Validation Gap (Prompt 03)

**Date:** 2026-08-21
**Prompt summary:** Implement `utils/file_handler.py` with full JSON validation.
**Defect fixed:** Initial draft of `_validate_card` only checked for key presence, not value type or emptiness. A card like `{"front": 42, "back": null}` would have been silently accepted. Added explicit `isinstance(value, str)` and `value.strip()` checks, and updated tests (`test_reject_empty_or_non_string_fields`, `test_reject_empty_string_front`) to cover these cases.

---

## Entry 4 — Adaptive Mode Infinite Loop Risk (Prompt 02 planning)

**Date:** 2026-08-21
**Prompt summary:** Design AdaptiveMode strategy.
**Logic corrected:** Identified that if a user always answers incorrectly, `AdaptiveMode` would loop indefinitely. The risk was mitigated by: (a) documenting it in the risk matrix, and (b) designing `mark_answer` to only re-queue on `correct=False` so the caller (quiz loop in `main.py`) controls exit via the `exit` command or `Ctrl+C`, giving the user agency without an infinite automated loop.

---

## Entry 5 — mypy strict mode with third-party stubs (Prompt 02)

**Date:** 2026-08-21
**Prompt summary:** Configure `mypy.ini` for the project.
**Prompt improved:** Initial plan used bare `strict = True` which caused `mypy` to error on `colorama` imports due to missing stubs. Resolved by adding `types-colorama` to `requirements.txt` and setting `ignore_missing_imports = True` in `mypy.ini` as a fallback for any other third-party libraries that lack stub packages.

---

## Entry 6 — sys.path Injection in Tests (Prompt 03)

**Date:** 2026-08-21
**Prompt summary:** Write `tests/test_flashcard_loader.py`.
**Correction made:** Tests import top-level modules (`exceptions`, `utils.file_handler`) that are not installed as a package. Added `sys.path.insert(0, ...)` at the top of the test file to ensure pytest can resolve imports regardless of working directory, avoiding `ModuleNotFoundError` during `pytest` runs.

---

## Entry 7 — RandomMode Testability Improvement (Prompt 04)

**Date:** 2026-08-21
**Prompt summary:** Implement Strategy and Factory patterns with required tests.
**Prompt improved:** The original `RandomMode.__init__` called `random.shuffle()` on the global RNG, making shuffle order non-deterministic and impossible to test for order correctness. Refactored to accept an optional `seed: Optional[int] = None` parameter and use a local `random.Random(seed)` instance. This enables fully deterministic tests (`test_random_mode_shuffles_with_seed`) while preserving true randomness in production use.

---

## Entry 8 — mypy Callable vs Type[QuizMode] for Factory Map (Prompt 04)

**Date:** 2026-08-21
**Prompt summary:** Type the factory `_MODE_MAP` dict correctly for mypy strict mode.
**Defect fixed:** Annotating `_MODE_MAP` as `Dict[str, Type[QuizMode]]` caused mypy to report "Cannot instantiate abstract class" at the call site `_MODE_MAP[key](cards)` because mypy treats `Type[QuizMode]` as the abstract class itself. Fixed by introducing a `_ModeFactory = Callable[[List[Flashcard]], QuizMode]` type alias and annotating the map as `Dict[str, _ModeFactory]`. This satisfies mypy strict mode while preserving the Factory pattern semantics.
