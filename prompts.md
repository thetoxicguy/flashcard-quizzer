# Prompts Record

Index of structured record of prompts used to direct the AI agent during development.

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
| 10.5 | 10.5-architecture-documentation | Documentation | Create docs/architecture.md: 10 sections, 6 Mermaid diagrams (high-level architecture flowchart, class diagram, factory selection flowchart, JSON loading activity diagram, session data flow diagram, quiz session sequence diagram); Strategy and Factory pattern documentation with problem/solution/diagram; 5 Architecture Decision Records; testing architecture section with component diagram and per-module coverage table; all diagrams generated from actual implementation |
| 11 | 11-final-definition-of-done-check | Release Gate | Execute final DoD: run all 7 automated commands (help, pytest, coverage, black, black --check, mypy, flake8); run 4 interactive smoke tests (sequential all-correct, adaptive with re-queuing, exit command, SIGINT/Ctrl+C); verify all 12 release criteria; all pass with no fixes required; 89/89 tests, 99% coverage, 21 ai_edit_log entries; 3 external environment limitations documented (not project defects) |

# Flashcard Quizzer - Structured AI Prompt Log

#### Note: All results as a consequence of these prompts have been reviewed and tested.

Use the prompts below in sequence. Each prompt is a complete JSON instruction for the AI coding agent. After every implementation prompt, require the agent to inspect its work, update `docs/ai_edit_log.md`, and run the listed verification commands.

---

## Prompt 01 - Analyze Requirements and Establish the Definition of Done

```json
{
  "prompt_id": "01-requirements-and-definition-of-done",
  "role": "Senior Python Software Architect and Quality Lead",
  "objective": "Analyze the Flashcard Quizzer requirements, define the implementation plan, and establish a verifiable Definition of Done before writing code.",
  "project": {
    "name": "Flashcard Quizzer",
    "language": "Python",
    "application_type": "Command Line Interface",
    "entry_point": "main.py"
  },
  "required_folder_structure": {
    "main.py": "Application entry point and argparse configuration.",
    "data/": "Sample JSON flashcard files, including glossary.json and python_basics.json.",
    "utils/": "Helper modules, including utils/file_handler.py.",
    "tests/": "Pytest test suite.",
    "docs/": "Documentation and AI interaction log templates; maintain docs/ai_edit_log.md.",
    ".env": "Configuration values for AI or development tools. Do not store secrets in source control.",
    "README.md": "Current setup instructions, usage, architecture, testing, and feature documentation.",
    "prompts.md": "Structured record of prompts used to direct the AI agent."
  },
  "functional_requirements": {
    "json_formats": [
      {
        "name": "array",
        "example": [{"front": "Term", "back": "Definition"}]
      },
      {
        "name": "object_wrapper",
        "example": {"cards": [{"front": "Term", "back": "Definition"}]}
      }
    ],
    "required_card_fields": ["front", "back"],
    "quiz_modes": ["sequential", "random", "adaptive"],
    "session_statistics": ["total questions", "accuracy percentage", "missed terms"],
    "graceful_errors": true,
    "raw_tracebacks_for_expected_user_errors": false
  },
  "design_requirements": {
    "strategy_pattern": {
      "abstract_base_class": "QuizMode",
      "implementations": ["SequentialMode", "RandomMode", "AdaptiveMode"]
    },
    "factory_pattern": "A factory must select the correct QuizMode implementation from the CLI mode value.",
    "modular_architecture": true,
    "type_hints_for_all_functions": true,
    "separation_of_concerns": true
  },
  "cli_requirements": {
    "parser": "argparse",
    "flags": {
      "-f_or_--file": "Path to the JSON flashcard file.",
      "-m_or_--mode": "Quiz mode: sequential, random, or adaptive.",
      "--stats": "Display session statistics."
    },
    "interaction": {
      "correct_color": "green",
      "incorrect_color": "red",
      "exit_command": "exit",
      "handle_ctrl_c": true,
      "quit_without_traceback": true
    }
  },
  "quality_assurance": {
    "tools_to_install_and_run": ["pytest", "pytest-cov", "black", "mypy", "flake8"],
    "minimum_test_coverage_percent": 90,
    "self_check_required": true
  },
  "definition_of_done": [
    "python main.py --help displays all available flags without errors.",
    "python main.py --mode sequential --file data/glossary.json starts a standard quiz without errors.",
    "python main.py -m adaptive -f data/python_basics.json allows a full playable quiz session.",
    "The implementation uses Strategy and Factory patterns and those patterns are visible when inspecting quiz_engine.py or its delegated mode module.",
    "python -m pytest tests/ passes.",
    "python -m pytest --cov=. --cov-report=html passes and reports more than 90 percent coverage.",
    "black --check . passes.",
    "mypy . passes.",
    "flake8 . passes with no linting errors.",
    "docs/ai_edit_log.md contains at least five specific examples of prompts improved, defects fixed, or logic corrected.",
    "README.md contains accurate setup instructions, commands, features, JSON formats, architecture, and testing instructions."
  ],
  "task": "Return a phased implementation plan, planned module responsibilities, dependency list, risks, and a Definition of Done checklist. Do not generate implementation code yet.",
  "output_requirements": {
    "format": "Markdown",
    "include_assumptions": true,
    "include_traceability_matrix": true,
    "include_verification_commands": true
  }
}
```

---

## Prompt 02 - Create the Project Skeleton and Development Configuration

```json
{
  "prompt_id": "02-project-skeleton",
  "role": "Lead Python Engineer",
  "objective": "Create the complete project skeleton and development configuration without implementing the full quiz behavior yet.",
  "context": {
    "entry_point": "main.py",
    "required_directories": ["data", "utils", "tests", "docs"],
    "required_initial_files": [
      "main.py",
      "quiz_engine.py",
      "models.py",
      "exceptions.py",
      "utils/__init__.py",
      "utils/file_handler.py",
      "tests/__init__.py",
      "docs/ai_edit_log.md",
      "data/glossary.json",
      "data/python_basics.json",
      ".env",
      ".gitignore",
      "README.md",
      "requirements.txt"
    ]
  },
  "implementation_requirements": {
    "type_hints": true,
    "docstrings": true,
    "modular_design": true,
    "no_single_file_solution": true,
    "do_not_commit_secrets": true,
    "env_file_handling": "Add .env to .gitignore or provide a safe .env.example if appropriate."
  },
  "dependencies": {
    "runtime": ["colorama"],
    "development": ["pytest", "pytest-cov", "black", "mypy", "flake8"]
  },
  "agent_actions": [
    "Create the required directories and files in accordance with the Implementation Plan.",
    "Always follow SOLID principles with Clean architecture",
    "Populate sample JSON data in both supported formats.",
    "Add dependency and tool configuration suitable for the project.",
    "Install the declared dependencies in the current environment.",
    "Record the generated structure and any corrections in docs/ai_edit_log.md."
  ],
  "verification_commands": [
    "python main.py --help",
    "python -m pytest tests/",
    "black --check .",
    "mypy .",
    "flake8 ."
  ],
  "self_check": {
    "required": true,
    "instruction": "Run every verification command that is applicable to the skeleton. Fix failures caused by generated files before reporting completion. Clearly report commands that are intentionally pending because later phases are not implemented."
  },
  "output_requirements": {
    "show_files_created": true,
    "show_commands_run": true,
    "show_command_results": true,
    "show_remaining_work": true
  }
}
```

---

## Prompt 03 - Phase 1: Data Layer and Validation

```json
{
  "prompt_id": "03-data-layer-and-validation",
  "role": "Senior Python Backend Engineer",
  "phase": "Phase 1 - Data Layer and Validation",
  "objective": "Implement a robust, typed flashcard data loader in utils/file_handler.py and any supporting model or exception modules.",
  "supported_json_formats": {
    "array_format": [{"front": "Question", "back": "Answer"}],
    "object_format": {"cards": [{"front": "Question", "back": "Answer"}]}
  },
  "validation_requirements": [
    "The root must be either a list of cards or an object containing a cards list.",
    "Every card must be an object.",
    "Every card must contain front and back fields.",
    "front and back must be non-empty strings.",
    "Reject unsupported root structures and malformed cards with a custom application exception.",
    "Handle missing files, unreadable files, malformed JSON, missing cards, and missing required fields.",
    "Expected user-facing failures must produce friendly messages and no raw Python traceback."
  ],
  "architecture": {
    "model": "Use a typed Flashcard model or dataclass.",
    "helper_module": "utils/file_handler.py",
    "custom_exceptions": true,
    "separation_from_cli": true
  },
  "required_tests": {
    "file": "tests/test_flashcard_loader.py",
    "test_cases": [
      "test_load_valid_flashcards_array",
      "test_load_valid_flashcards_object_wrapper",
      "test_load_invalid_json",
      "test_load_missing_required_field",
      "test_load_missing_file",
      "test_reject_empty_or_non_string_fields"
    ]
  },
  "quality_gate": {
    "install_if_missing": ["pytest", "pytest-cov", "black", "mypy", "flake8"],
    "commands": [
      "python -m pytest tests/test_flashcard_loader.py",
      "black .",
      "black --check .",
      "mypy .",
      "flake8 ."
    ],
    "fix_generated_issues_before_completion": true
  },
  "documentation": {
    "update": "docs/ai_edit_log.md",
    "log_content": "Record the original approach, validation issues discovered, prompt refinements, and corrections made."
  },
  "output_requirements": {
    "provide_complete_file_changes": true,
    "provide_test_results": true,
    "provide_quality_tool_results": true,
    "do_not_claim_success_without_running_commands": true
  }
}
```

---

## Prompt 04 - Phase 2: Strategy and Factory Patterns

```json
{
  "prompt_id": "04-strategy-and-factory-patterns",
  "role": "Principal Python Engineer",
  "phase": "Phase 2 - Core Logic and Design Patterns",
  "objective": "Implement the quiz ordering logic using the Strategy Pattern and select strategies using the Factory Pattern.",
  "architecture_requirements": {
    "abstract_base_class": {
      "name": "QuizMode",
      "mechanism": "abc.ABC",
      "responsibility": "Define the common interface for ordering or selecting flashcards."
    },
    "strategies": [
      {
        "name": "SequentialMode",
        "behavior": "Return cards in their original order from 1 through N."
      },
      {
        "name": "RandomMode",
        "behavior": "Return cards in shuffled order without mutating the caller's original collection."
      },
      {
        "name": "AdaptiveMode",
        "behavior": "Prioritize or repeat cards answered incorrectly while ensuring the session can progress and terminate."
      }
    ],
    "factory": {
      "responsibility": "Return the correct QuizMode object for sequential, random, or adaptive input.",
      "invalid_mode_behavior": "Raise a friendly, specific application error."
    },
    "location": "Keep the pattern implementation inspectable from quiz_engine.py, either directly or through clearly imported delegated modules."
  },
  "engineering_constraints": [
    "Use type hints for all functions and methods.",
    "Use dependency injection or deterministic random seeding where it improves testability.",
    "Follow the Open/Closed Principle.",
    "Do not mix terminal input or colored output into mode-selection algorithms."
  ],
  "required_tests": {
    "file": "tests/test_quiz_modes.py",
    "test_cases": [
      "test_quiz_mode_factory",
      "test_factory_rejects_invalid_mode",
      "test_sequential_mode_order",
      "test_random_mode_preserves_cards",
      "test_adaptive_mode_behavior"
    ]
  },
  "quality_gate": {
    "commands": [
      "python -m pytest tests/test_quiz_modes.py",
      "black .",
      "black --check .",
      "mypy .",
      "flake8 ."
    ],
    "require_all_to_pass": true
  },
  "documentation": {
    "update": "docs/ai_edit_log.md",
    "minimum_examples_progress": "Ensure the cumulative log is moving toward at least five concrete prompt improvements or logic corrections."
  },
  "output_requirements": {
    "explain_pattern_roles": true,
    "show_files_changed": true,
    "show_test_and_quality_results": true
  }
}
```

---

## Prompt 05 - Implement the Quiz Engine and Session Statistics

```json
{
  "prompt_id": "05-quiz-engine-and-statistics",
  "role": "Senior Python Application Engineer",
  "objective": "Implement the quiz session engine independently from argparse and terminal rendering.",
  "functional_requirements": [
    "Present the front of each flashcard.",
    "Accept text answers through an injectable input function or UI abstraction.",
    "Compare answers case-insensitively and ignore surrounding whitespace.",
    "Return immediate correct or incorrect outcomes to the UI layer.",
    "Track total questions, correct answers, incorrect answers, accuracy percentage, and missed terms.",
    "Support SequentialMode, RandomMode, and AdaptiveMode through the same QuizMode interface.",
    "AdaptiveMode must prioritize or repeat incorrect cards in a verifiable way.",
    "Avoid division-by-zero errors for empty or interrupted sessions.",
    "Allow a session to terminate cleanly when the UI signals exit."
  ],
  "design_constraints": {
    "business_logic_only": true,
    "argparse_independent": true,
    "terminal_color_independent": true,
    "fully_typed": true,
    "testable_without_real_user_input": true
  },
  "required_tests": {
    "files": ["tests/test_quiz_engine.py", "tests/test_quiz_modes.py"],
    "scenarios": [
      "Case-insensitive correct answer.",
      "Incorrect answer is captured in missed terms.",
      "Accuracy is calculated correctly.",
      "Adaptive mode revisits an incorrect card.",
      "An interrupted or empty session returns safe statistics."
    ]
  },
  "quality_gate": {
    "commands": [
      "python -m pytest tests/",
      "black .",
      "black --check .",
      "mypy .",
      "flake8 ."
    ],
    "fix_failures_before_completion": true
  },
  "documentation": {
    "update": "docs/ai_edit_log.md",
    "record": "Document logic errors found during self-review and how the implementation or prompt was corrected."
  },
  "output_requirements": {
    "show_implementation_summary": true,
    "show_commands_and_results": true,
    "identify_any_remaining_risks": true
  }
}
```

---

## Prompt 06 - Phase 3: CLI and User Interaction

```json
{
  "prompt_id": "06-cli-and-interaction",
  "role": "Python CLI and User Experience Engineer",
  "phase": "Phase 3 - CLI and Interaction",
  "objective": "Build the user-facing command-line interface in main.py using argparse and connect it to the validated data layer and quiz engine.",
  "cli_requirements": {
    "parser": "argparse",
    "flags": [
      {
        "short": "-f",
        "long": "--file",
        "purpose": "Select the flashcard JSON file."
      },
      {
        "short": "-m",
        "long": "--mode",
        "choices": ["sequential", "random", "adaptive"],
        "purpose": "Select the quiz mode."
      },
      {
        "long": "--stats",
        "purpose": "Display session statistics."
      }
    ],
    "help_requirement": "python main.py --help must display every available flag and valid mode.",
    "supported_equivalent_commands": [
      "python main.py --mode sequential --file data/glossary.json",
      "python main.py -m adaptive -f data/python_basics.json"
    ]
  },
  "interaction_requirements": [
    "Display correct feedback in green.",
    "Display incorrect feedback in red.",
    "Allow the user to type exit to stop the quiz.",
    "Catch KeyboardInterrupt so Ctrl+C exits gracefully without a traceback.",
    "Display friendly messages for file, validation, and mode errors.",
    "Display a final summary containing total questions, accuracy percentage, and missed terms.",
    "Make standard CLI execution possible without importing internal modules manually."
  ],
  "implementation_constraints": {
    "keep_cli_thin": true,
    "do_not_duplicate_engine_logic": true,
    "type_hints": true,
    "portable_color_handling": true
  },
  "verification_commands": [
    "python main.py --help",
    "python main.py --mode sequential --file data/glossary.json",
    "python main.py -m adaptive -f data/python_basics.json"
  ],
  "quality_gate": {
    "commands": [
      "python -m pytest tests/",
      "black .",
      "black --check .",
      "mypy .",
      "flake8 ."
    ],
    "require_self_check": true
  },
  "documentation": {
    "update": "docs/ai_edit_log.md",
    "record": "Document CLI defects, usability improvements, and corrections made after running the application."
  },
  "output_requirements": {
    "show_help_output_summary": true,
    "show_interactive_smoke_test_method": true,
    "show_quality_results": true
  }
}
```

---

## Prompt 07 - Build the Required Comprehensive Test Suite

```json
{
  "prompt_id": "07-comprehensive-tests",
  "role": "Senior Software Development Engineer in Test",
  "objective": "Create and run the complete pytest suite required for the final submission.",
  "test_files": {
    "tests/test_flashcard_loader.py": [
      "test_load_valid_flashcards_array",
      "test_load_valid_flashcards_object_wrapper",
      "test_load_invalid_json",
      "test_load_missing_required_field"
    ],
    "tests/test_quiz_modes.py": [
      "test_quiz_mode_factory",
      "test_adaptive_mode_behavior"
    ],
    "tests/test_integration.py": [
      "test_full_session"
    ]
  },
  "integration_test_requirements": {
    "test_full_session": "Simulate a user answering three questions and verify total questions, correct and incorrect counts, accuracy, and missed terms.",
    "no_manual_input": true,
    "deterministic": true
  },
  "additional_test_expectations": [
    "Test both supported JSON root formats.",
    "Test missing files and malformed JSON.",
    "Test missing front or back fields.",
    "Test case-insensitive comparison.",
    "Test factory invalid-mode behavior.",
    "Test graceful exit and Ctrl+C handling where practical.",
    "Test argparse help and primary command paths without launching uncontrolled interactive input."
  ],
  "coverage": {
    "target": "greater than 90 percent",
    "commands": [
      "python -m pytest tests/",
      "python -m pytest --cov=. --cov-report=html"
    ],
    "instruction": "If coverage is 90 percent or lower, inspect uncovered lines and branches, add meaningful tests, and rerun until coverage is greater than 90 percent. Do not add tests that only execute lines without asserting behavior."
  },
  "quality_gate": {
    "commands": [
      "black .",
      "black --check .",
      "mypy .",
      "flake8 ."
    ],
    "require_all_to_pass": true
  },
  "documentation": {
    "update": "docs/ai_edit_log.md",
    "record": "Document test failures, coverage gaps, and the prompt or implementation changes used to resolve them."
  },
  "output_requirements": {
    "show_test_summary": true,
    "show_exact_coverage_percentage": true,
    "show_uncovered_risk_areas": true,
    "show_all_quality_results": true
  }
}
```

---

## Prompt 08 - Perform an Engineering Review Before Refactoring

```json
{
  "prompt_id": "08-engineering-review",
  "role": "Staff Software Engineer and Code Reviewer",
  "objective": "Inspect the complete implementation and produce findings before modifying code.",
  "review_scope": [
    "Functional requirements",
    "Data validation for both JSON formats",
    "Friendly error handling without expected tracebacks",
    "Strategy Pattern correctness",
    "Factory Pattern correctness",
    "Adaptive mode termination and incorrect-card prioritization",
    "argparse flags and help output",
    "CLI exit and Ctrl+C behavior",
    "Statistics correctness",
    "Type-hint completeness",
    "Separation of concerns",
    "Test quality and coverage",
    "README accuracy",
    "AI edit log completeness",
    "Security of .env and secrets"
  ],
  "review_instructions": {
    "inspect_actual_files": true,
    "identify_logic_errors": true,
    "identify_hallucinated_or_unused_imports": true,
    "identify_code_smells": true,
    "identify_missing_tests": true,
    "do_not_modify_code_yet": true
  },
  "required_runtime_checks": [
    "python main.py --help",
    "python -m pytest tests/",
    "python -m pytest --cov=. --cov-report=html",
    "black --check .",
    "mypy .",
    "flake8 ."
  ],
  "output_requirements": {
    "format": "Prioritized review report",
    "severity_levels": ["blocker", "high", "medium", "low"],
    "include_file_and_symbol": true,
    "include_reproduction_or_evidence": true,
    "include_recommended_fix": true,
    "include_definition_of_done_status": true
  }
}
```

---

## Prompt 09 - Refactor and Correct the Reviewed Implementation

```json
{
  "prompt_id": "09-refactor-and-correct",
  "role": "Principal Python Engineer",
  "objective": "Apply the engineering review findings while preserving correct external behavior and satisfying every acceptance criterion.",
  "goals": [
    "Correct all blocker and high-severity defects.",
    "Correct meaningful medium and low findings where safe.",
    "Reduce coupling and duplication.",
    "Improve cohesion, readability, and testability.",
    "Preserve Strategy and Factory pattern clarity.",
    "Preserve both long and short CLI flags.",
    "Preserve support for both JSON formats.",
    "Preserve friendly error and graceful-exit behavior."
  ],
  "constraints": {
    "do_not_remove_required_features": true,
    "do_not_weaken_tests": true,
    "do_not_lower_coverage_threshold": true,
    "fully_typed": true,
    "update_tests_for_legitimate_behavior_changes": true
  },
  "self_verification": {
    "commands": [
      "python main.py --help",
      "python -m pytest tests/",
      "python -m pytest --cov=. --cov-report=html",
      "black .",
      "black --check .",
      "mypy .",
      "flake8 ."
    ],
    "require_all_to_pass": true,
    "coverage_requirement": "greater than 90 percent"
  },
  "documentation": {
    "update": "docs/ai_edit_log.md",
    "minimum_entries": 5,
    "entry_requirements": [
      "Original prompt or approach",
      "Problem discovered",
      "Improved prompt or corrected logic",
      "Result after verification"
    ]
  },
  "output_requirements": {
    "show_findings_resolved": true,
    "show_files_changed": true,
    "show_verification_results": true,
    "show_remaining_nonblocking_risks": true
  }
}
```

---

## Prompt 10 - Generate and Validate README.md

```json
{
  "prompt_id": "10-readme",
  "role": "Senior Technical Writer with Python Engineering Experience",
  "objective": "Create an accurate README.md based on the actual implemented and tested project.",
  "required_sections": [
    "Project Overview",
    "Features",
    "Folder Structure",
    "Requirements",
    "Installation",
    "Environment Configuration",
    "Supported JSON Formats",
    "CLI Flags",
    "Running the Application",
    "Quiz Modes",
    "Session Statistics",
    "Running Tests",
    "Generating the Coverage Report",
    "Formatting, Type Checking, and Linting",
    "Architecture and Design Patterns",
    "Graceful Exit Behavior",
    "AI Interaction Log"
  ],
  "required_commands": [
    "python main.py --help",
    "python main.py --mode sequential --file data/glossary.json",
    "python main.py -m adaptive -f data/python_basics.json",
    "python -m pytest tests/",
    "python -m pytest --cov=. --cov-report=html",
    "black --check .",
    "mypy .",
    "flake8 ."
  ],
  "accuracy_constraints": [
    "Document only commands and features that exist in the repository.",
    "Do not claim quality tools pass unless they were run successfully.",
    "Explain both array and object-wrapper JSON formats with valid examples.",
    "Explain that .env must not contain committed secrets."
  ],
  "verification": {
    "run_documented_commands": true,
    "correct_inaccurate_documentation": true,
    "update_ai_log": true
  },
  "output_requirements": {
    "write_file": "README.md",
    "report_documented_commands_verified": true
  }
}
```

---
## Prompt 10.5 - Generate Architecture Documentation with Mermaid
```json
{
  "prompt_id": "10.5-architecture-documentation",
  "role": "Principal Software Architect and Technical Writer",
  "objective": "Create professional architecture documentation that accurately reflects the implemented Flashcard Quizzer application.",
  "context": {
    "project_name": "Flashcard Quizzer",
    "language": "Python",
    "application_type": "CLI Application"
  },
  "documentation_output": {
    "file": "docs/architecture.md",
    "format": "Markdown"
  },
  "instruction": {
    "inspect_actual_codebase": true,
    "do_not_assume_structure": true,
    "generate_diagrams_from_existing_implementation": true,
    "explain_design_decisions": true
  },
  "required_sections": [
    "System Overview",
    "Architecture Goals",
    "Project Structure",
    "Module Responsibilities",
    "Design Patterns",
    "Data Flow",
    "Application Lifecycle",
    "Error Handling Strategy",
    "Testing Architecture",
    "Extensibility Considerations"
  ],
  "mermaid_diagrams": [
    {
      "name": "High Level Architecture",
      "type": "flowchart",
      "description": "Show user interaction, CLI layer, quiz engine, quiz modes, data loader, JSON files, and output."
    },
    {
      "name": "Component Diagram",
      "type": "flowchart",
      "description": "Show module dependencies between main.py, quiz_engine.py, file_handler.py, models.py, and tests."
    },
    {
      "name": "Class Diagram",
      "type": "classDiagram",
      "description": "Show Flashcard model, QuizMode abstract class, SequentialMode, RandomMode, AdaptiveMode, QuizModeFactory, QuizEngine and relationships."
    },
    {
      "name": "Quiz Session Sequence Diagram",
      "type": "sequenceDiagram",
      "description": "Show execution flow from application start through question answering and statistics generation."
    },
    {
      "name": "JSON Loading Activity Diagram",
      "type": "flowchart",
      "description": "Show validation flow, supported formats, exception handling, and flashcard creation."
    },
    {
      "name": "Adaptive Mode Workflow",
      "type": "flowchart",
      "description": "Show how incorrect cards are tracked and prioritized."
    }
  ],
  "required_design_pattern_documentation": {
    "strategy_pattern": {
      "describe_problem": true,
      "describe_solution": true,
      "identify_abstractions": true,
      "identify_concrete_strategies": true,
      "include_mermaid_class_relationships": true
    },
    "factory_pattern": {
      "describe_problem": true,
      "describe_solution": true,
      "show_factory_selection_logic": true,
      "include_diagram": true
    }
  },
  "architecture_decisions": [
    {
      "topic": "Strategy Pattern",
      "question": "Why was Strategy Pattern selected?"
    },
    {
      "topic": "Factory Pattern",
      "question": "Why is Factory Pattern beneficial here?"
    },
    {
      "topic": "Modular Design",
      "question": "Why separate CLI, engine, data loading, and models?"
    },
    {
      "topic": "Type Hints",
      "question": "How do type hints improve maintainability?"
    },
    {
      "topic": "Testing",
      "question": "How does the architecture support high test coverage?"
    }
  ],
  "required_mermaid_examples": {
    "high_level_architecture": true,
    "class_diagram": true,
    "sequence_diagram": true,
    "data_flow_diagram": true
  },
  "quality_requirements": {
    "documentation_matches_implementation": true,
    "all_diagrams_render_in_mermaid": true,
    "no_unused_components_in_diagrams": true,
    "diagram_labels_are_clear": true,
    "include_legend_when_helpful": true
  },
  "verification": {
    "compare_documentation_against_code": true,
    "ensure_all_modules_are_documented": true,
    "ensure_all_patterns_are_documented": true
  },
  "deliverables": [
    "docs/architecture.md",
    "Mermaid High-Level Architecture Diagram",
    "Mermaid Class Diagram",
    "Mermaid Sequence Diagram",
    "Mermaid Data Flow Diagram",
    "Strategy Pattern Documentation",
    "Factory Pattern Documentation",
    "Architecture Decision Records"
  ],
  "output_requirements": {
    "include_complete_markdown": true,
    "include_all_mermaid_blocks": true,
    "include_explanatory_text": true,
    "include_design_pattern_analysis": true
  }
}
```

---

## Prompt 11 - Final Automated Definition of Done Check

```json
{
  "prompt_id": "11-final-definition-of-done-check",
  "role": "Release Engineer and Quality Gatekeeper",
  "objective": "Execute the final Definition of Done and fix any project-owned failure before declaring the project complete.",
  "preconditions": [
    "All implementation phases are complete.",
    "All required tests exist.",
    "README.md and docs/ai_edit_log.md are current."
  ],
  "commands_to_run": [
    "python main.py --help",
    "python -m pytest tests/",
    "python -m pytest --cov=. --cov-report=html",
    "black .",
    "black --check .",
    "mypy .",
    "flake8 ."
  ],
  "interactive_smoke_tests": [
    {
      "command": "python main.py --mode sequential --file data/glossary.json",
      "expected": "The quiz starts, accepts answers, displays colored feedback, and shows statistics without errors."
    },
    {
      "command": "python main.py -m adaptive -f data/python_basics.json",
      "expected": "A full adaptive game can be played and incorrectly answered cards are prioritized or repeated."
    },
    {
      "action": "Type exit during a quiz",
      "expected": "The application exits cleanly without a traceback."
    },
    {
      "action": "Press Ctrl+C during a quiz",
      "expected": "The application exits cleanly without a traceback."
    }
  ],
  "release_criteria": {
    "help_lists_all_flags": true,
    "standard_quiz_command_works": true,
    "adaptive_quiz_command_works": true,
    "strategy_pattern_present": true,
    "factory_pattern_present": true,
    "all_tests_pass": true,
    "coverage_greater_than_90_percent": true,
    "black_check_passes": true,
    "mypy_passes": true,
    "flake8_passes": true,
    "ai_edit_log_has_at_least_5_entries": true,
    "readme_is_current": true
  },
  "failure_policy": "Do not state that the project is complete if any release criterion fails. Diagnose and fix generated code, tests, configuration, or documentation, then rerun the affected checks and the full quality gate.",
  "output_requirements": {
    "provide_pass_fail_checklist": true,
    "include_exact_command_results": true,
    "include_exact_coverage_percentage": true,
    "include_unresolved_external_limitations": true
  }
}
```

---

## Prompt 12 - Final Principal Engineer Audit

```json
{
  "prompt_id": "12-final-principal-engineer-audit",
  "role": "Principal Engineer and Project Evaluator",
  "objective": "Audit the finished repository against the complete project rubric and reject unsupported completion claims.",
  "audit_categories": {
    "data_layer": [
      "Loads array-format JSON.",
      "Loads object-wrapper JSON.",
      "Validates front and back.",
      "Handles malformed JSON and missing files with friendly messages."
    ],
    "core_logic": [
      "QuizMode abstract base class exists.",
      "SequentialMode, RandomMode, and AdaptiveMode inherit from QuizMode.",
      "Factory returns the correct mode.",
      "Adaptive behavior prioritizes or repeats incorrect questions."
    ],
    "cli": [
      "argparse supports -f/--file, -m/--mode, and --stats.",
      "--help displays all flags.",
      "Correct answers are green and incorrect answers are red.",
      "exit and Ctrl+C quit gracefully."
    ],
    "testing": [
      "Required named tests exist.",
      "Full session integration test simulates three answers and validates statistics.",
      "All tests pass.",
      "Coverage is greater than 90 percent."
    ],
    "quality": [
      "black --check . passes.",
      "mypy . passes.",
      "flake8 . passes.",
      "Type hints are present throughout the application."
    ],
    "documentation": [
      "README.md contains current setup and feature descriptions.",
      "docs/ai_edit_log.md contains at least five prompt improvements or logic corrections.",
      "prompts.md records the structured prompt workflow."
    ]
  },
  "evidence_requirements": {
    "inspect_repository": true,
    "run_commands": true,
    "do_not_accept_claims_without_evidence": true,
    "cite_file_paths_and_test_names": true
  },
  "output": {
    "pass_fail_checklist": true,
    "remaining_gaps": true,
    "recommended_fixes": true,
    "final_release_decision": true
  }
}
```

---

## Bonus Prompt - Critical Hiring Manager Review

```json
{
  "prompt_id": "bonus-hiring-manager-review",
  "role": "Senior Python Hiring Manager",
  "objective": "Review the finished project as an engineering portfolio submission after all formal quality gates pass.",
  "evaluation_criteria": [
    "Code Quality",
    "Architecture",
    "Strategy Pattern",
    "Factory Pattern",
    "Error Handling",
    "CLI Usability",
    "Testing Quality",
    "Maintainability",
    "Documentation",
    "Production Readiness"
  ],
  "instructions": {
    "be_critical_but_evidence_based": true,
    "identify_rejection_reasons": true,
    "separate_required_fixes_from_optional_improvements": true,
    "do_not_invent_missing_evidence": true
  },
  "output_requirements": {
    "strengths": true,
    "risks": true,
    "required_fixes": true,
    "optional_improvements": true,
    "portfolio_readiness_decision": true
  }
}
```
