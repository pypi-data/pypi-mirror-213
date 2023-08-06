"""Prompt helpers."""

from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.validation import Validator

from .pprint import pprint


def prompt_choice(prompt_text: str, choices: list[str]):
    choices_str = ", ".join(choices)
    pprint(f"<prompt>{prompt_text}</prompt>: {choices_str}")

    completer = FuzzyWordCompleter(choices)
    validator = Validator.from_callable(
        lambda x: x in choices,
        error_message="Invalid account",
        move_cursor_to_end=True,
    )

    return prompt(
        "> ",
        default=choices[0],
        completer=completer,
        validator=validator,
    )
