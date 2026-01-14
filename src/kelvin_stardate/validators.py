# src/kelvin_stardate/validators.py

"""
Pure validation + parsing helpers for kelvin_stardate.

This module must NOT:
- print()
- input()
- reference color helpers
- call CLI help callbacks

It MAY:
- raise StardateCLIError with specific error codes/messages
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional, Tuple

from .errors import StardateCLIError


# ============================================================
# Month name lookup (shared by CLI parsing)
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
# Basic string guards (CLI calls check_user_input separately)
# ============================================================

def require_not_none(value: Optional[str]) -> str:
    if value is None:
        raise StardateCLIError("E001", "Empty input.")
    return value


def require_non_empty(value: str) -> str:
    s = value.strip()
    if s == "":
        raise StardateCLIError("E001", "Input cannot be empty.")
    return value


# ============================================================
# Earth date field parsing (ported from prompts.py)
# ============================================================

def parse_year(value: str) -> int:
    """
    Strict numeric years only for Earth dates.
    Rules:
      - digits only
      - 1..9999 range (datetime.date limits)
      - no decimals
    """
    require_not_none(value)
    require_non_empty(value)
    raw = value.strip()

    if "." in raw:
        raise StardateCLIError("E007", f"Invalid year '{value}' (must be an integer).")

    if not raw.isdigit():
        raise StardateCLIError("E007", f"Invalid year '{value}' (numeric only).")

    y = int(raw)
    if not (1 <= y <= 9999):
        raise StardateCLIError("E008", f"Year '{y}' out of range 1–9999.")

    return y


def parse_year_yyyy(value: str) -> int:
    """
    Strict 4-digit year input (YYYY).
    """
    require_not_none(value)
    require_non_empty(value)
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
    require_not_none(value)
    require_non_empty(value)
    raw = value.strip().lower()

    if raw in MONTH_LOOKUP:
        return MONTH_LOOKUP[raw]

    if raw.isdigit():
        m = int(raw)
        if 1 <= m <= 12:
            return m
        raise StardateCLIError("E002", f"Invalid numeric month '{raw}'")

    raise StardateCLIError("E002", f"Unrecognized month '{value}'")


def parse_day(value: str) -> int:
    require_not_none(value)
    require_non_empty(value)
    raw = value.strip()

    if not raw.isdigit():
        # you currently use E002 here even though it’s a day; preserving behavior
        raise StardateCLIError("E002", f"Invalid day '{value}'")

    d = int(raw)
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
    """
    require_not_none(date_str)
    require_non_empty(date_str)
    raw_date = date_str.strip()

    parts = raw_date.split("-")
    if len(parts) != 3:
        raise StardateCLIError("E012", f"Invalid date '{date_str}'. Expected YYYY-MM-DD.")

    y_raw, m_raw, d_raw = parts
    y = parse_year(y_raw)
    m = parse_month(m_raw)
    d = parse_day(d_raw)

    if is_leap_year_fn is not None and m == 2 and d == 29 and not is_leap_year_fn(y):
        raise StardateCLIError("E003", f"{y} is not a leap year.")

    return y, m, d


# ============================================================
# Stardate validation (ported from prompts.py)
# ============================================================

def validate_stardate_string(sd_str: str) -> str:
    """
    Strict stardate formatting + sanity bounds:
      - must NOT look like an Earth date
      - requires exactly one decimal
      - digits on both sides
      - numeric only
      - year must be 4 digits (0001–9999)
      - fractional part length <= 8
    """
    require_not_none(sd_str)
    require_non_empty(sd_str)
    s = sd_str.strip()

    if "-" in s:
        raise StardateCLIError("E011", "Stardate must not contain '-' (Earth date detected).")

    if "." not in s:
        raise StardateCLIError("E005", "Stardate must contain a decimal (e.g., 2258.042).")

    if s.count(".") != 1:
        raise StardateCLIError("E011", "Stardate must contain exactly one decimal point.")

    left, right = s.split(".", 1)

    if left == "" or right == "":
        raise StardateCLIError("E011", "Stardate must have digits on both sides of the decimal.")

    if not left.isdigit() or not right.isdigit():
        raise StardateCLIError("E011", f"Invalid stardate '{sd_str}' (numeric only).")

    if len(left) != 4:
        raise StardateCLIError(
            "E011",
            f"Invalid stardate '{sd_str}' (year must be 4 digits, e.g., 2258.042)."
        )

    year = int(left)
    if not (1 <= year <= 9999):
        raise StardateCLIError("E011", f"Invalid stardate '{sd_str}' (year out of range 0001–9999).")

    if len(right) > 8:
        raise StardateCLIError("E011", f"Invalid stardate '{sd_str}' (fractional part too long).")

    return s


def validate_kelvin_stardate_string(sd_str: str) -> str:
    """
    Kelvin-format stardate:
      - YYYY.DDD (exactly 3-digit ordinal)
      - ordinal must be 001–366
    """
    s = validate_stardate_string(sd_str)
    _, right = s.split(".", 1)

    if len(right) != 3:
        raise StardateCLIError(
            "E011",
            f"Invalid Kelvin stardate '{sd_str}' (expected 3-digit ordinal, e.g., 2258.042)."
        )

    ordinal = int(right)
    if not (1 <= ordinal <= 366):
        raise StardateCLIError(
            "E011",
            f"Invalid Kelvin stardate '{sd_str}' (ordinal day must be 001–366)."
        )

    return s


# ============================================================
# Mode detector
# ============================================================

def detect_stardate_type(sd: str) -> str:
    """
    Returns:
      - "kelvin" for 1–3 digits after decimal (or non-numeric frac)
      - "astronomical" for >=4 digits after decimal
    """
    s = sd.strip()
    try:
        _, frac = s.split(".", 1)
    except ValueError:
        return "kelvin"

    if not frac.isdigit():
        return "kelvin"

    return "astronomical" if len(frac) >= 4 else "kelvin"
