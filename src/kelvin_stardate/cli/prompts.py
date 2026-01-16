# src/kelvin_stardate/cli/prompts.py
# kelvin_cli_input.py (v1.5-)

"""
CLI-only input utilities.

Responsibilities:
- help/quit/empty handling (via check_user_input)  [CLI UX]
- interactive prompting helpers (reprompt loops)   [CLI UX]
- NO argparse wiring
- NO result printing tables
- NO pure validation logic (moved to validators.py)

All parsing/validation is imported from kelvin_stardate.validators
so it can be reused by other interfaces later (MVC-ish separation).
"""

from __future__ import annotations

from typing import Callable, Optional, Tuple, TypeVar

from ..errors import StardateCLIError
from ..cli.colors import c, reset

T = TypeVar("T")


# ============================================================
# CONTROL EXCEPTION (help-trigger re-prompt)
# ============================================================

class ContinuePrompt(Exception):
    """Raised after help is shown to restart the prompt."""
    pass


# ============================================================
# HELP + QUIT + EMPTY HANDLER
# ============================================================

def check_user_input(value: str, help_cb: Optional[Callable[[], None]] = None) -> str:
    """
    Handles:
      - quit commands (q/quit/exit)
      - help commands (h/help) -> calls help_cb, then triggers ContinuePrompt
      - empty input

    NOTE: help_cb is passed in from the CLI to avoid circular imports.
    """
    if value is None:
        raise StardateCLIError("E001", "Empty input.")

    stripped = value.strip().lower()

    # Quit
    if stripped in ("q", "-q", "/q", "quit", "exit"):
        print(f"\n{c('info')}Goodbye!{reset()}\n")
        raise SystemExit

    # Help
    if stripped in ("h", "/h", "-h", "--help", "-help", "help", "/help"):
        if help_cb:
            help_cb()
        raise ContinuePrompt

    # Empty string
    if stripped == "":
        raise StardateCLIError("E001", "Input cannot be empty.")

    return value


# ============================================================
# PROMPT HELPERS (interactive reprompt loops)
# ============================================================

def prompt_until_valid(
    prompt: str,
    parser_func: Callable[[str], T],
    *,
    help_cb: Optional[Callable[[], None]] = None,
    error_printer: Optional[Callable[[StardateCLIError], None]] = None,
    reprompt: str = " > ",
) -> T:
    """
    Simple-style prompting:
      - shows `prompt` only on the first attempt
      - after an error, shows `reprompt` (default: " > ")
      - prints errors (either via error_printer or a default formatter)
      - supports help/quit via check_user_input

    parser_func should raise StardateCLIError for user-facing validation errors.
    If parser_func raises ValueError, we wrap it to keep UX consistent.
    """
    first = True
    while True:
        try:
            raw = input(prompt if first else reprompt)
            first = False

            check_user_input(raw, help_cb=help_cb)
            return parser_func(raw)

        except ContinuePrompt:
            first = False
            continue

        except StardateCLIError as err:
            if error_printer:
                error_printer(err)
            else:
                print(f"{c('error')}Error [{err.code}]: {err.msg}{reset()}")

        except ValueError as err:
            wrapped = StardateCLIError("E002", str(err) or "Invalid value.")
            if error_printer:
                error_printer(wrapped)
            else:
                print(f"{c('error')}Error [{wrapped.code}]: {wrapped.msg}{reset()}")


def prompt_menu_choice(
    prompt: str,
    valid: Tuple[str, ...],
    *,
    help_cb: Optional[Callable[[], None]] = None,
    error_printer: Optional[Callable[[StardateCLIError], None]] = None,
    reprompt: str = " > ",
    code: str = "E009",
    msg: str = "Invalid selection. Please select 1 or 2."
) -> str:
    """
    Menu choice prompt with minimal reprompting.
    """
    first = True
    while True:
        try:
            raw = input(prompt if first else reprompt)
            first = False

            check_user_input(raw, help_cb=help_cb)
            s = raw.strip()
            if s in valid:
                return s

            raise StardateCLIError(code, msg)

        except ContinuePrompt:
            first = False
            continue

        except StardateCLIError as err:
            if error_printer:
                error_printer(err)
            else:
                print(f"{c('error')}Error [{err.code}]: {err.msg}{reset()}")


def prompt_yes_no(
    prompt: str,
    *,
    help_cb: Optional[Callable[[], None]] = None,
    error_printer: Optional[Callable[[StardateCLIError], None]] = None,
    reprompt: str = " > ",
) -> bool:
    """
    Yes/No prompt that returns a boolean.
    """
    first = True
    while True:
        try:
            raw = input(prompt if first else reprompt)
            first = False

            check_user_input(raw, help_cb=help_cb)
            s = raw.strip().lower()
            if s in ("y", "yes"):
                return True
            if s in ("n", "no"):
                return False

            raise StardateCLIError("E010", "Please enter y/n (or yes/no).")

        except ContinuePrompt:
            first = False
            continue

        except StardateCLIError as err:
            if error_printer:
                error_printer(err)
            else:
                print(f"{c('error')}Error [{err.code}]: {err.msg}{reset()}")
