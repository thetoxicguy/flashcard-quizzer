# Reflective Report: Collaborating with AI Tools in Software Development

## Introduction

The development history of Flashcard Quizzer offers a useful case study in AI-assisted software engineering. The project is small, but the collaboration was not treated as a sequence of casual code-generation requests. The prompts established requirements, architecture, risks, tests, quality gates, and documentation obligations. The edit log then recorded where the generated implementation was incomplete, misleading, or difficult to test, and how those issues were corrected. Together, `prompts.md` and `docs/ai_edit_log.md` show that productive collaboration with an AI tool depends less on asking for code quickly and more on creating a disciplined feedback loop around the code.

The central lesson is that an AI assistant is most valuable as an active engineering partner when its output is constrained by explicit intent and challenged by executable evidence. It can propose structure, identify likely defects, and accelerate implementation, but human judgment remains essential for deciding whether behavior is actually correct, maintainable, and useful to a person running the application.

## Prompts as Engineering Specifications

The prompt sequence was effective because it moved from definition to implementation in deliberate phases. Prompt 01 established the project architecture, functional requirements, design patterns, quality tools, risks, and Definition of Done before implementation began. Later prompts narrowed the focus: data validation, strategy and factory patterns, the quiz engine, the CLI, comprehensive tests, review, refactoring, and documentation. This sequencing reduced ambiguity and gave the AI a stable frame of reference.

The prompts also specified observable outcomes rather than relying only on vague qualities such as "clean code." For example, the data-layer prompt required support for two JSON shapes and explicitly listed malformed JSON, missing files, missing fields, empty strings, and non-string values as cases to handle. The CLI prompt specified `exit`, `Ctrl+C`, colored feedback, friendly errors, and an always-visible summary. These details made it possible to evaluate the implementation against behavior that a user could observe.

Another strength was the repeated requirement to inspect the work, update the edit log, and run verification commands. That turned each prompt into a small engineering contract. The prompts did not merely ask the AI to produce files; they asked it to demonstrate that the files worked. This is an important collaboration pattern: requirements, implementation, self-review, and evidence should travel together.

## What Review and Testing Revealed

The edit log makes clear that first-pass generation was useful but not sufficient. Several defects were found only when the implementation was tested closely or reviewed as a system.

The file handler initially checked whether `front` and `back` keys existed, but accepted values such as `42` and `null`. The correction added type and non-empty-string validation, followed by tests for those exact cases. This illustrates why requirements must describe valid values, not just required names. It also demonstrates a productive division of labor: the AI can generate a plausible validation path, while tests expose the difference between structural validity and semantic validity.

The random quiz mode produced another important lesson. Calling the global random generator made order-dependent tests nondeterministic. Introducing an optional seed and a local `random.Random` instance preserved production randomness while enabling deterministic verification. This is a broader principle for AI collaboration: when a generated design is hard to test, ask how dependencies can be injected or controlled. Testability is not a secondary convenience; it often reveals whether responsibilities have been separated properly.

The quiz engine was improved in a similar way. An initial design mixed session state mutation, looping, input, and presentation concerns. Redesigning `run_session` as a generator with an injectable `input_fn` separated business logic from `argparse`, terminal rendering, and `colorama`. Tests could then provide scripted answers without monkey-patching real input. This made the code easier to reason about and made the user interface a replaceable boundary rather than an assumption embedded in the engine.

The later engineering review found subtler issues that ordinary happy-path tests might miss. A dead `_current` field in `AdaptiveMode` created misleading state. Two mode lists duplicated the same source of truth and could drift apart. `AnswerResult` claimed to be immutable but used `__slots__`, which does not prevent reassignment. The generator yielded the same mutable `SessionStats` object repeatedly, so stored results could all appear to have the final state. Each correction improved not just correctness but the accuracy of the design's story. Good software should not merely work; its names, types, and documentation should tell the truth.

## The Human Role in AI-Assisted Development

This history argues against both extremes of AI use. The assistant is not an autonomous developer whose output can be accepted without inspection, but it is also more than a typing shortcut. Its best contribution is to expand the number of design possibilities considered quickly and to help carry out repetitive implementation work. The human contribution is to define priorities, notice contradictions, challenge assumptions, and judge whether the result serves the actual user.

The AdaptiveMode discussion is a good example. The risk of an endless sequence of incorrect answers was recognized during planning. The chosen behavior allowed incorrect cards to be re-queued while leaving termination to the caller through `exit` or `Ctrl+C`. That decision involves user agency and product behavior, not just syntax. An AI can enumerate options, but a human must decide what “progress” and “termination” should mean for this application.

The same applies to coverage. A first coverage run showed that `main.py` had zero percent coverage because subprocess tests did not instrument the child process. Direct unit tests were added, raising the file to 98 percent and total project coverage to 99 percent. Yet the team did not pretend that 99 percent meant perfection. The final log documented the untested `__main__` guard and a display branch, as well as the environment limitation that quality tools were available through `python -m` but not directly on the system path. This is a model of honest automation: metrics are evidence, not a substitute for judgment.

## Collaboration Practices That Generalize

Several practices from this project transfer well to larger systems.

First, define a Definition of Done before implementation. It should include behavior, architecture, tests, documentation, and commands that can be run. This prevents the AI from optimizing for a locally complete file while missing project-level obligations.

Second, ask for narrow phases with explicit boundaries. The prompts separated the loader, mode strategies, engine, CLI, tests, review, and documentation. Smaller scopes make failures easier to localize and reduce the chance that an assistant will silently redesign unrelated parts of the system.

Third, require adversarial cases early. Empty values, malformed input, invalid modes, repeated incorrect answers, interrupted sessions, mutable references, and nondeterministic randomness are more informative than another happy-path example. These cases force the collaboration toward robustness.

Fourth, use tools as a conversation partner. Pytest, coverage, mypy, Black, and Flake8 each answered a different question. Tests checked behavior, coverage exposed neglected paths, mypy challenged type assumptions, and formatting and linting enforced consistency. The AI's response should change when evidence contradicts its first explanation.

Finally, maintain a decision record. The edit log preserved not only what changed but why it changed. This creates institutional memory, makes the process auditable, and helps distinguish deliberate tradeoffs from accidental behavior. The prompt record complements it by showing how requests evolved from planning through release validation.

## Limits and Remaining Risks

The focus is not to eliminate AI-generated proposals, but to make their acceptance conditional. Every meaningful claim should have an appropriate check: a test, a type check, a command, a manual smoke test, or a clearly recorded assumption. When a check is unavailable, the uncertainty should be named rather than hidden.

## Conclusion

Flashcard Quizzer demonstrates a mature pattern for collaborating with AI tools: specify intent precisely, implement in bounded stages, inspect the result, test behavior at the edges, review the design for misleading state and duplication, document corrections, and finish with a release gate. The AI accelerated construction and helped surface alternatives, but the quality of the outcome came from the surrounding discipline.

The deepest lesson is that collaboration works when the AI is given enough structure to be useful and enough scrutiny to remain accountable. Prompts define the direction, code turns that direction into a concrete artifact, and verification determines whether the artifact deserves trust. That loop produces better software than either uncritical automation or purely manual work, because it combines speed with deliberate engineering judgment.
