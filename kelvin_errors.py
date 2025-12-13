# kelvin_errors.py

"""
Error handling and error-code registry for the Kelvin stardate CLI.

Provides:
  - ErrorInfo: structured metadata for each error code.
  - ERROR_REGISTRY: mapping from code -> ErrorInfo.
  - StardateCLIError: main exception type for CLI-level errors.
  - helper functions to format errors for CLI and help screens.
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ErrorInfo:
    code: str
    short: str          # brief, user-facing message (CLI)
    long: str           # more detailed explanation (help)
    dev: Optional[str]  # optional dev notes for debugging / internals


# TODO:
# -- Reorder error codes in REGISTRY view so empty/null-style errors appear first
#    when listing, even if their code numbers are larger.
# -- The CLI currently hard-codes some codes (e.g. "E007" for empty input).
#    Once things stabilize, we can refactor to a more declarative mapping
#    between situations and codes.
# -- Add a dev-mode flag in the CLI to show `dev` messages in addition to `long`
#    when printing or logging errors.


# ============================================================
# RENAMBERED ERROR CODES
# E001 is now EMPTY INPUT (formerly E007)
# Everything else shifts down by 1 in numbering, but retains meaning
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
}


# ============================================================
# Exception + helper functions (unchanged)
# ============================================================

class StardateCLIError(Exception):
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

    # fallback: include anything not in preferred_order
    for code in ERROR_REGISTRY:
        if code not in preferred_order:
            ordered.append(ERROR_REGISTRY[code])

    return ordered
