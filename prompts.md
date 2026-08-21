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
