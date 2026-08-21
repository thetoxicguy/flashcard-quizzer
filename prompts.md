# Prompts Record

Structured record of prompts used to direct the AI agent during development.

| # | Prompt ID | Phase | Summary |
|---|-----------|-------|---------|
| 1 | 01-requirements-and-definition-of-done | Planning | Define implementation plan, module responsibilities, risks, and DoD checklist |
| 2 | 02-project-skeleton | Scaffold | Create directories, placeholder modules, config files, sample data, install deps |
| 3 | 03-data-layer-and-validation | Phase 1 | Implement file_handler.py, models, exceptions, and full test suite |
| 4 | 04-strategy-and-factory-patterns | Phase 2 | Implement QuizMode ABC, SequentialMode, RandomMode, AdaptiveMode, and get_quiz_mode() factory; add seed param for testability; write tests/test_quiz_modes.py |
| 5 | 05-quiz-engine-and-statistics | Phase 3 | Implement run_session() generator with injectable input_fn, AnswerResult, _answers_match(); refactor main.py to use run_session(); write tests/test_quiz_engine.py |
| 6 | 06-cli-and-interaction | Phase 4 | Verify and harden main.py CLI: --help, green/red feedback, exit command, KeyboardInterrupt, friendly errors, always-on compact summary + --stats detailed breakdown |
| 7 | 07-comprehensive-tests | Phase 5 | Write tests/test_integration.py and tests/test_main.py; fill coverage gaps in main.py and file_handler.py; achieve 99% coverage (89 tests passing); all quality gates clean |
| 8 | 08-engineering-review | Review | Full codebase inspection; 6 findings (0 blockers, 0 high, 3 medium, 3 low); all DoD criteria met; identified: dead _current field, shared SessionStats reference, VALID_MODES duplication, AnswerResult immutability claim, annotation width, missing README items |
| 9 | 09-refactor-and-correct | Refactor | Apply all 6 engineering review findings: remove dead AdaptiveMode._current field; fix SessionStats shared-reference bug via dataclasses.replace(); derive SUPPORTED_MODES from _MODE_MAP eliminating VALID_MODES duplication; convert AnswerResult to frozen dataclass for enforced immutability; widen _extract_card_list annotation to Any; update README with setup.cfg entry and 99% coverage; add ai_edit_log entries 14–19; all 89 tests pass, 99% coverage, all quality gates clean |
| 10 | 10-readme | Documentation | Rewrite README.md as a comprehensive technical reference: 17 sections covering features, folder structure, requirements, installation, .env config, both JSON formats with examples, CLI flags with verified --help output, running examples with session transcript, all three quiz modes, session statistics, graceful exit table, test-file breakdown table, coverage report with setup.cfg snippet, quality-gate section with verified commands (python -m black/mypy/flake8), architecture and design patterns, AI interaction log; all documented commands verified before writing; ai_edit_log entry 20 added |
