# kelvin_cli_input.py
"""
CLI-only input utilities for kelvin_stardate_cli.py

Responsibilities:
- parsing (year/month/day, earth-date strings, stardate strings)
- interactive prompting helpers (reprompt loops)
- help/quit/empty handling (via check_user_input)
- NO argparse wiring
- NO result printing tables
"""

from __future__ import annotations

from typing import Callable, Optional, Tuple

from kelvin_errors import StardateCLIError
from kelvin_colors import c, reset


# ============================================================
# CONTROL EXCEPTION (help-trigger re-prompt)
# ============================================================

class ContinuePrompt(Exception):
    """Raised after help is shown to restart the prompt."""
    pass


# ============================================================
# MONTH NAME LOOKUP
# ============================================================
MONTH_LOOKUP = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}


# ============================================================
# HELP + QUIT + EMPTY HANDLER
# TODO: ADD RED ERROR STYLING WHERE NECESSARY
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
    if stripped in ("h", "/h", "-h", "-help", "help", "/help"):
        if help_cb:
            help_cb()
        raise ContinuePrompt

    # Empty string
    if stripped == "":
        raise StardateCLIError("E001", "Input cannot be empty.")

    return value


# ============================================================
# PARSERS
# MONTH + DAY + YEAR
# ============================================================

def parse_year(value: str) -> int:
    """
    Strict numeric years only for Earth dates.
    Suggested rules:
      - digits only
      - 1..9999 range (datetime.date limits)
      - no decimals
    """
    check_user_input(value)
    raw_year_v = value.strip()

    if "." in raw_year_v:
        raise StardateCLIError("E007", f"Invalid year '{value}' (must be an integer).")

    if not raw_year_v.isdigit():
        raise StardateCLIError("E007", f"Invalid year '{value}' (numeric only).")

    y = int(raw_year_v)
    if not (1 <= y <= 9999):
        raise StardateCLIError("E008", f"Year '{y}' out of range 1–9999.")

    return y


def parse_month(value: str) -> int:
    check_user_input(value)
    raw_month_v = value.strip().lower()

    if raw_month_v in MONTH_LOOKUP:
        return MONTH_LOOKUP[raw_month_v]

    if raw_month_v.isdigit():
        m = int(raw_month_v)
        if 1 <= m <= 12:
            return m
        raise StardateCLIError("E002", f"Invalid numeric month '{raw_month_v}'")

    raise StardateCLIError("E002", f"Unrecognized month '{value}'")


def parse_day(value: str) -> int:
    check_user_input(value)
    raw_day_v = value.strip()

    if not raw_day_v.isdigit():
        raise StardateCLIError("E002", f"Invalid day '{value}'")

    d = int(raw_day_v)
    if not (1 <= d <= 31):
        raise StardateCLIError("E002", f"Day '{d}' out of range 1–31")

    return d


def parse_earth_date(
    date_str: str,
    *,
    is_leap_year_fn: Optional[Callable[[int], bool]] = None
) -> Tuple[int, int, int]:
    """
    Accepts:
      - YYYY-MM-DD
      - YYYY-mon-DD (mon = jan/feb/...)

    NOTE: takes is_leap_year_fn injected from kelvin_stardate.py to avoid
    importing library-level rules here.
    """
    check_user_input(date_str)
    raw_date = date_str.strip()

    parts = raw_date.split("-")
    if len(parts) != 3:
        raise StardateCLIError("E012", f"Invalid date '{date_str}'. Expected YYYY-MM-DD.")

    y_raw, m_raw, d_raw = parts
    y = parse_year(y_raw)
    m = parse_month(m_raw)
    d = parse_day(d_raw)

    # preserve nicer leap-year semantics (E003) instead of generic date ValueError.
    if is_leap_year_fn is not None and m == 2 and d == 29 and not is_leap_year_fn(y):
        raise StardateCLIError("E003", f"{y} is not a leap year.")

    return y, m, d

# ============================================================
# VALIDATION HELPERS
# ============================================================
def validate_stardate_string(sd_str: str) -> str:
    """
    Strict stardate formatting:
      - exactly one decimal
      - digits on both sides
      - no other characters
    """
    check_user_input(sd_str)
    s = sd_str.strip()

    if s.count(".") != 1:
        raise StardateCLIError("E011", "Stardate must contain exactly one decimal point (e.g., 2258.042).")

    left, right = s.split(".", 1)
    if left == "" or right == "":
        raise StardateCLIError("E011", "Stardate must have digits on both sides of the decimal.")
    if not left.isdigit() or not right.isdigit():
        raise StardateCLIError("E011", f"Invalid stardate '{sd_str}' (numeric only).")

    return s


# ============================================================
# PROMPT HELPERS (interactive reprompt loops)
# ============================================================

def prompt_until_valid(
    prompt: str,
    parser_func: Callable[[str], object],
    *,
    help_cb: Optional[Callable[[], None]] = None,
    error_printer: Optional[Callable[[StardateCLIError], None]] = None
):
    """
    Re-prompts until parser_func succeeds.
    error_printer is injected from CLI so this module stays UI-agnostic.
    """
    while True:
        try:
            raw = input(prompt)
            check_user_input(raw, help_cb=help_cb)
            return parser_func(raw)
        except ContinuePrompt:
            continue
        except StardateCLIError as err:
            if error_printer:
                error_printer(err)


def prompt_menu_choice(
    prompt: str,
    valid: Tuple[str, ...],
    *,
    help_cb: Optional[Callable[[], None]] = None,
    error_printer: Optional[Callable[[StardateCLIError], None]] = None,
    code: str = "E009",
    msg: str = "Invalid selection."
) -> str:
    while True:
        try:
            raw = input(prompt)
            check_user_input(raw, help_cb=help_cb)
            s = raw.strip()
            if s in valid:
                return s
            raise StardateCLIError(code, msg)
        except ContinuePrompt:
            continue
        except StardateCLIError as err:
            if error_printer:
                error_printer(err)


def prompt_yes_no(
    prompt: str,
    *,
    help_cb: Optional[Callable[[], None]] = None,
    error_printer: Optional[Callable[[StardateCLIError], None]] = None
) -> bool:
    while True:
        try:
            raw = input(prompt)
            check_user_input(raw, help_cb=help_cb)
            s = raw.strip().lower()
            if s in ("y", "yes"):
                return True
            if s in ("n", "no"):
                return False
            raise StardateCLIError("E010", "Please enter y/n (or yes/no).")
        except ContinuePrompt:
            continue
        except StardateCLIError as err:
            if error_printer:
                error_printer(err)
