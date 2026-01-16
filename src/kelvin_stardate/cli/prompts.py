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
"""

from __future__ import annotations

from typing import Callable, Optional, Tuple, TypeVar

from ..errors import StardateCLIError
from ..cli.colors import c, reset

T = TypeVar("T")

class ContinuePrompt(Exception):
    """Raised after help is shown to restart the prompt."""
    pass


def check_user_input(value: str, help_cb: Optional[Callable[[], None]] = None) -> str:
    """
    Handles:
      - quit commands (q/quit/exit)
      - help commands (h/help) -> calls help_cb, then triggers ContinuePrompt
      - empty input
    """
    if value is None:
        raise StardateCLIError("E001", "Empty input.")

    stripped = value.strip().lower()

    if stripped in ("q", "-q", "/q", "quit", "exit"):
        print(f"\n{c('info')}Goodbye!{reset()}\n")
        raise SystemExit

    if stripped in ("h", "/h", "-h", "--help", "-help", "help", "/help"):
        if help_cb:
            help_cb()
        raise ContinuePrompt

    if stripped == "":
        raise StardateCLIError("E001", "Input cannot be empty.")

    return value


def prompt_until_valid(
    prompt: str,
    parser_func: Callable[[str], T],
    *,
    help_cb: Optional[Callable[[], None]] = None,
    error_printer: Optional[Callable[[StardateCLIError], None]] = None,
    reprompt: str = " > ",
) -> T:
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
