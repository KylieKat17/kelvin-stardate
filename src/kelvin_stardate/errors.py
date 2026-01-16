# src/kelvin_stardate/errors.py
# (formerly kelvin_errors.py v1.5-)

"""
Error handling and error-code registry for the Kelvin stardate tool.

Provides:
  - ErrorInfo: structured metadata for each error code.
  - ERROR_REGISTRY: mapping from code -> ErrorInfo.
  - StardateError: base exception type for library-level errors.
  - StardateCLIError: exception type for CLI-level, coded errors.
  - helper functions to format errors for CLI and help screens.
"""

from dataclasses import dataclass
from typing import Dict, Optional


# ============================================================
# Base error types
# ============================================================

class StardateError(Exception):
    """Base exception for the Kelvin stardate library/tool."""


@dataclass
class ErrorInfo:
    code: str
    short: str          # brief, user-facing message (CLI)
    long: str           # more detailed explanation (help)
    dev: Optional[str]  # optional dev notes for debugging / internals


# ============================================================
# ERROR REGISTRY
# ============================================================

ERROR_REGISTRY: Dict[str, ErrorInfo] = {

    # --------------------------------------------------------
    # E001 — Empty or null input (formerly E007)
    # --------------------------------------------------------
    "E001": ErrorInfo(
        code="E001",
        short="Input cannot be empty.",
        long=(
            "You pressed Enter without typing anything when the program asked "
            "for a value. The converter needs a valid year, month, day, or "
            "stardate string to work with."
        ),
        dev=(
            "Raised when stripped input is an empty string or None. Typically "
            "comes from check_user_input in the CLI layer."
        ),
    ),

    # --------------------------------------------------------
    # E002 — Invalid month value (formerly E001)
    # --------------------------------------------------------
    "E002": ErrorInfo(
        code="E002",
        short="Invalid month value.",
        long=(
            "The month you entered is either outside the valid range (1–12), "
            "or the month name/abbreviation could not be recognized.\n\n"
            "Examples of accepted names:\n"
            "  jan, january, feb, february, mar, march, sept, september, etc."
        ),
        dev=(
            "Raised when parse_month fails to normalize the month string into "
            "an integer between 1 and 12."
        ),
    ),

    # --------------------------------------------------------
    # E003 — Invalid day / month-year combination (formerly E002)
    # --------------------------------------------------------
    "E003": ErrorInfo(
        code="E003",
        short="Day or date is not valid for the given month/year.",
        long=(
            "The day you entered is outside the allowed range (1–31), or it "
            "does not make sense for the specific month and year.\n\n"
            "For example:\n"
            "  - April 31 is invalid (April has only 30 days).\n"
            "  - February 30 is invalid in all calendars.\n"
        ),
        dev=(
            "Raised when datetime.date(...) fails or when custom validation "
            "logic determines the day-month-year combination is invalid."
        ),
    ),

    # --------------------------------------------------------
    # E004 — Leap-day misuse (formerly E003)
    # --------------------------------------------------------
    "E004": ErrorInfo(
        code="E004",
        short="Invalid leap-day usage.",
        long=(
            "You tried to use February 29 in a year that is not a leap year "
            "under the Gregorian rules:\n"
            "  • divisible by 4 ⇒ leap year\n"
            "  • divisible by 100 ⇒ NOT a leap year\n"
            "  • divisible by 400 ⇒ leap year again\n"
        ),
        dev=(
            "Raised when 29 February is provided for a non-leap-year. The CLI "
            "may surface this directly or via E003 depending on context."
        ),
    ),

    # --------------------------------------------------------
    # E005 — Invalid stardate format (unchanged E005)
    # --------------------------------------------------------
    "E005": ErrorInfo(
        code="E005",
        short="Invalid stardate format.",
        long=(
            "A Kelvin-style stardate must include a decimal point, such as "
            "2258.42, not just '2258'. The part after the decimal expresses "
            "a fraction of the year/day sequence."
        ),
        dev=(
            "Raised when stardate parsing fails basic structural checks, "
            "including missing decimal, alphabetic characters, empty frac, "
            "or unexpected formatting."
        ),
    ),

    # --------------------------------------------------------
    # E006 — Unknown / unsupported conversion mode (formerly E008)
    # --------------------------------------------------------
    "E006": ErrorInfo(
        code="E006",
        short="Unknown conversion mode.",
        long=(
            "The mode you provided could not be mapped to any supported "
            "conversion mode.\n\n"
            "Supported values and common aliases:\n"
            "  • no_leap, noleap, nl, 1\n"
            "  • gregorian, greg, gr, 2\n"
            "  • astronomical, astro, astr, 3\n"
            "  • all, a, 4\n"
        ),
        dev=(
            "Raised when normalize_mode() cannot map a given mode string or "
            "integer to a known mode."
        ),
    ),
    
        # --------------------------------------------------------
    # E007 — Invalid year format
    # --------------------------------------------------------
    "E007": ErrorInfo(
        code="E007",
        short="Invalid year format.",
        long=(
            "The year you entered is not valid.\n\n"
            "Rules:\n"
            "  • Digits only (no letters or symbols)\n"
            "  • No decimal points\n"
            "  • Must be exactly four digits when requested (YYYY)"
        ),
        dev=(
            "Raised by parse_year() or parse_year_yyyy() when the input "
            "contains non-numeric characters, decimals, or the wrong length."
        ),
    ),

    # --------------------------------------------------------
    # E008 — Year out of supported range
    # --------------------------------------------------------
    "E008": ErrorInfo(
        code="E008",
        short="Year out of supported range.",
        long=(
            "The year you entered is outside the supported range.\n\n"
            "Valid years must be between 0001 and 9999, inclusive.\n"
            "This limit is imposed by Python's date system and timeline constraints."
        ),
        dev=(
            "Raised when a parsed year is numeric but outside the 1–9999 range."
        ),
    ),

    # --------------------------------------------------------
    # E009 — Invalid menu selection
    # --------------------------------------------------------
    "E009": ErrorInfo(
        code="E009",
        short="Invalid menu selection.",
        long=(
            "The option you selected is not valid for this menu.\n\n"
            "Please choose one of the listed options exactly as shown "
            "(for example: 1 or 2)."
        ),
        dev=(
            "Raised by prompt_menu_choice() when the user input does not match "
            "any of the allowed menu values."
        ),
    ),

    # --------------------------------------------------------
    # E010 — Invalid yes/no response
    # --------------------------------------------------------
    "E010": ErrorInfo(
        code="E010",
        short="Invalid yes/no response.",
        long=(
            "The program expected a yes-or-no answer.\n\n"
            "Accepted values:\n"
            "  • y / yes\n"
            "  • n / no"
        ),
        dev=(
            "Raised by prompt_yes_no() when input is not recognized as a "
            "boolean-style response."
        ),
    ),

    # --------------------------------------------------------
    # E011 — Invalid stardate format or value
    # --------------------------------------------------------
    "E011": ErrorInfo(
        code="E011",
        short="Invalid stardate.",
        long=(
            "The stardate you entered is not valid.\n\n"
            "Kelvin-format stardates must:\n"
            "  • Contain exactly one decimal point\n"
            "  • Use a 4-digit year (0001–9999)\n"
            "  • Use numeric digits only\n"
            "  • Not resemble an Earth date (no '-')\n\n"
            "Examples:\n"
            "  ✓ 2258.042\n"
            "  ✗ 2258-02-11\n"
            "  ✗ 2258.4.2"
        ),
        dev=(
            "Raised by validate_stardate_string() or "
            "validate_kelvin_stardate_string() when structural, numeric, "
            "or range checks fail."
        ),
    ),

    # --------------------------------------------------------
    # E012 — Invalid Earth date string format
    # --------------------------------------------------------
    "E012": ErrorInfo(
        code="E012",
        short="Invalid Earth date format.",
        long=(
            "The Earth date you entered is not in a recognized format.\n\n"
            "Accepted formats:\n"
            "  • YYYY-MM-DD\n"
            "  • YYYY-mon-DD  (month names or abbreviations)\n\n"
            "Examples:\n"
            "  ✓ 2258-02-11\n"
            "  ✓ 2258-feb-11\n"
            "  ✗ 2258/02/11"
        ),
        dev=(
            "Raised by parse_earth_date() when the input string does not split "
            "into exactly three components using '-' as a delimiter."
        ),
    ),
}


# ============================================================
# CLI-level coded exception + helper functions
# ============================================================

class StardateCLIError(StardateError):
    """
    CLI-focused error that carries an error code + registry metadata.
    Inherits StardateError so callers can catch either broad or specific errors.
    """
    def __init__(self, code: str, msg: Optional[str] = None):
        self.code = code
        self.info = ERROR_REGISTRY.get(code)

        if msg is not None:
            self.msg = msg
        elif self.info:
            self.msg = self.info.short
        else:
            self.msg = f"Unregistered error code: {code}"

        super().__init__(self.msg)

    def __str__(self):
        return f"Error [{self.code}]: {self.msg}"


def get_error_info(code: str) -> Optional[ErrorInfo]:
    return ERROR_REGISTRY.get(code)


def format_error_for_cli(err: StardateCLIError) -> str:
    return f"Error [{err.code}]: {err.msg}"


def format_error_for_help(code: str, dev_mode: bool = False) -> str:
    info = ERROR_REGISTRY.get(code)
    if not info:
        return f"{code}: (no registry entry found)"

    if not dev_mode:
        return f"{code}: {info.long}"

    if info.dev:
        return f"{code}: {info.long}\n\n[DEV]\n{info.dev}"
    return f"{code}: {info.long}"


def list_error_codes_ordered():
    """
    Order for human help display:
      1. E001 (empty input)
      2. E002 (invalid month)
      3. E003 (invalid day)
      4. E004 (leap day)
      5. E005 (stardate format)
      6. E006 (unknown mode)
    """
    preferred_order = ["E001", "E002", "E003", "E004", "E005", "E006"]

    ordered = []
    for code in preferred_order:
        if code in ERROR_REGISTRY:
            ordered.append(ERROR_REGISTRY[code])

    # fallback: includes anything not in preferred_order
    for code in ERROR_REGISTRY:
        if code not in preferred_order:
            ordered.append(ERROR_REGISTRY[code])

    return ordered