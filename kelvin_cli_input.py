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

from typing import Callable, Optional, Tuple, TypeVar

from kelvin_errors import StardateCLIError
from kelvin_colors import c, reset

T = TypeVar("T")


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
# PARSERS
# MONTH + DAY + YEAR
# ============================================================

def parse_year(value: str) -> int:
    """
    Strict numeric years only for Earth dates.
    Rules:
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

def parse_year_yyyy(value: str) -> int:
    """
    Strict 4-digit year input (YYYY).
    Useful for CLI UX when prompt explicitly says (YYYY).
    """
    check_user_input(value)
    raw = value.strip()

    if "." in raw:
        raise StardateCLIError("E007", f"Invalid year '{value}' (must be an integer).")

    if not raw.isdigit():
        raise StardateCLIError("E007", f"Invalid year '{value}' (numeric only).")

    if len(raw) != 4:
        raise StardateCLIError("E007", f"Invalid year '{value}' (expected 4 digits, YYYY).")

    y = int(raw)
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
    Strict stardate formatting + sanity bounds:
      - must NOT look like an Earth date
      - requires exactly one decimal
      - digits on both sides
      - numeric only
      - year must be 4 digits (0001–9999) to match Python library and Kelvin timeline expectations
      - fractional part length must be reasonable to avoid overflow paths
    """
    check_user_input(sd_str)
    s = sd_str.strip()

    # --- Earth date accidentally entered ---
    if "-" in s:
        raise StardateCLIError(
            "E011",
            "Stardate must not contain '-' (Earth date detected)."
        )

    # --- Missing decimal entirely ---
    if "." not in s:
        raise StardateCLIError(
            "E005",
            "Stardate must contain a decimal (e.g., 2258.042)."
        )

    # --- Too many decimals ---
    if s.count(".") != 1:
        raise StardateCLIError(
            "E011",
            "Stardate must contain exactly one decimal point."
        )

    left, right = s.split(".", 1)

    # --- Decimal present but malformed ---
    if left == "" or right == "":
        raise StardateCLIError(
            "E011",
            "Stardate must have digits on both sides of the decimal."
        )

    # --- Non-numeric characters ---
    if not left.isdigit() or not right.isdigit():
        raise StardateCLIError(
            "E011",
            f"Invalid stardate '{sd_str}' (numeric only)."
        )

    # --- Kelvin timeline sanity: year must be 4 digits (0001–9999) ---
    if len(left) != 4:
        raise StardateCLIError(
            "E011",
            f"Invalid stardate '{sd_str}' (year must be 4 digits, e.g., 2258.042)."
        )

    year = int(left)
    if not (1 <= year <= 9999):
        raise StardateCLIError(
            "E011",
            f"Invalid stardate '{sd_str}' (year out of range 0001–9999)."
        )

    # --- Prevent absurdly long fractional parts (keeps float/date math safe) ---
    # Kelvin stardates are typically 3 digits; astronomical uses 4+.
    # Allow up to 8 to be generous, but block extreme inputs that can cause overflow.
    if len(right) > 8:
        raise StardateCLIError(
            "E011",
            f"Invalid stardate '{sd_str}' (fractional part too long)."
        )

    return s


def validate_kelvin_stardate_string(sd_str: str) -> str:
    """
    Kelvin-format stardate:
      - YYYY.DDD (DDD = ordinal day, 001–365/366-ish depending on interpretation)
      - exactly 4-digit year
      - exactly 3-digit fractional ordinal
    """
    s = validate_stardate_string(sd_str)  # uses existing sanity checks
    left, right = s.split(".", 1)

    if len(right) != 3:
        raise StardateCLIError(
            "E011",
            f"Invalid Kelvin stardate '{sd_str}' (expected 3-digit ordinal, e.g., 2258.042)."
        )

    # Enforce ordinal range 001–366 (helps UX a lot)
    ordinal = int(right)
    if not (1 <= ordinal <= 366):
        raise StardateCLIError(
            "E011",
            f"Invalid Kelvin stardate '{sd_str}' (ordinal day must be 001–366)."
        )

    return s


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
      - always prints errors (either via error_printer or a default formatter)
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
            # help was shown; re-prompt (keep minimal reprompt feel)
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
    Menu choice prompt with minimal reprompting
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
