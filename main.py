"""Flashcard Quizzer — CLI entry point."""

import argparse
import sys
from typing import Callable, Optional

import colorama
from colorama import Fore, Style

from exceptions import FlashcardError, InvalidModeError
from models import Flashcard, SessionStats
from quiz_engine import display_stats, get_quiz_mode, run_session
from utils.file_handler import load_flashcards

colorama.init(autoreset=True)

VALID_MODES = ["sequential", "random", "adaptive"]


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="flashcard-quizzer",
        description="Quiz yourself with flashcards from a JSON file.",
    )
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        metavar="FILE",
        help="Path to the JSON flashcard file.",
    )
    parser.add_argument(
        "-m",
        "--mode",
        default="sequential",
        choices=VALID_MODES,
        metavar="MODE",
        help=f"Quiz mode: {', '.join(VALID_MODES)}. (default: sequential)",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Display session statistics at the end.",
    )
    return parser


def _make_input_fn(
    prompt_prefix: str,
) -> Callable[[Flashcard], Optional[str]]:
    """Return a terminal input function that prints the card front and reads a line.

    Args:
        prompt_prefix: Label printed before the answer prompt (e.g. "A: ").

    Returns:
        A callable suitable for passing to ``run_session``.
    """

    def _input(card: Flashcard) -> Optional[str]:
        print(f"Q: {card.front}")
        try:
            return input(prompt_prefix)
        except EOFError:
            return None

    return _input


def run_quiz(args: argparse.Namespace) -> None:
    """Load cards, run the quiz loop, and optionally display stats.

    Args:
        args: Parsed CLI arguments.
    """
    try:
        cards = load_flashcards(args.file)
    except FlashcardError as exc:
        print(f"{Fore.RED}Error: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        mode = get_quiz_mode(args.mode, cards)
    except InvalidModeError as exc:
        print(f"{Fore.RED}Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(
        f"Starting {args.mode} quiz with {len(cards)} card(s). "
        "Type 'exit' to quit.\n"
    )

    stats = SessionStats()
    for result, stats in run_session(mode, _make_input_fn("A: ")):
        if result.correct:
            print(Fore.GREEN + "Correct!")
        else:
            print(Fore.RED + f"Incorrect. The answer is: {result.card.back}")
        print()

    if args.stats:
        display_stats(stats)


def main() -> None:
    """Parse arguments and start the quiz."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        run_quiz(args)
    except KeyboardInterrupt:
        print(f"\n{Style.BRIGHT}Quiz interrupted. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
