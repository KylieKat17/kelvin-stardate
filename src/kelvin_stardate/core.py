# core.py
# kelvin_stardate.py (v1.5-)

from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Union

class StardateError(Exception):
    pass


# ================================
#   Utilities
# ================================

def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def day_of_year(dt: date) -> int:
    """Return 1-based ordinal day."""
    return dt.timetuple().tm_yday


def format_ordinal(ord_day: int) -> str:
    """Screenplay-accurate 2- or 3-digit ordinal formatting."""
    if ord_day < 1:
        raise StardateError("Ordinal day must be >= 1.")
    if ord_day < 100:
        return f"{ord_day:02d}"
    return f"{ord_day:03d}"


# ================================
#   KelvinStardate Object
# ================================

@dataclass(frozen=True)
class KelvinStardate:
    year: int
    ordinal_day: int

    def __str__(self):
        return f"{self.year}.{format_ordinal(self.ordinal_day)}"

    @classmethod
    def parse(cls, s: str) -> "KelvinStardate":
        """
        Parse Kelvin-format ordinal stardates:
            2258.42  → 42nd day
            2258.4   → 4th day (auto-padded)
        """
        if "." not in s:
            raise StardateError("Kelvin stardate must contain a decimal point")

        year_str, ord_str = s.split(".", 1)
        year = int(year_str)

        if not ord_str.isdigit():
            raise StardateError(f"Ordinal part must be numeric: {ord_str}")
        ordinal = int(ord_str)

        return cls(year, ordinal)


# ================================
#   Earth → Stardate (Modes)
# ================================

def earth_to_stardate(
    dt: date,
    leap_mode: str = "no_leap",
) -> KelvinStardate:
    """
    Convert Earth date to Kelvin ordinal stardate.
    Modes:
       - 'no_leap'    : Orci 1..365 system
       - 'gregorian'  : ISO ordinal with leap days
       - 'astronomical' : Fractional system (returns float, not KelvinStardate)
    """
    if leap_mode == "astronomical":
        return earth_to_stardate_astronomical(dt)

    # Gregorian ordinal
    greg = day_of_year(dt)

    if leap_mode == "gregorian":
        ordinal = greg
    elif leap_mode == "no_leap":
        if is_leap_year(dt.year) and dt > date(dt.year, 2, 28):
            ordinal = greg - 1
        else:
            ordinal = greg
    else:
        raise StardateError(f"Unknown leap_mode: {leap_mode}")

    return KelvinStardate(year=dt.year, ordinal_day=ordinal)


def earth_to_stardate_astronomical(dt: date) -> float:
    """
    Continuous fractional Orci-like 'scientific' mode.
    """
    doy = day_of_year(dt)
    fraction = doy / 365.2425
    return round(dt.year + fraction, 5)


# ================================
#   Stardate → Earth (Modes)
# ================================

def stardate_to_earth(sd: Union[KelvinStardate, str, float],
                      leap_mode: str = "no_leap") -> date:
    """
    Convert stardate to Earth date.
    - If astronomical: sd must be float
    """
    if leap_mode == "astronomical":
        if isinstance(sd, (str, KelvinStardate)):
            raise StardateError("Astronomical mode requires float stardate input")
        return stardate_to_earth_astronomical(sd)

    # Kelvin ordinal modes
    if isinstance(sd, str):
        sd = KelvinStardate.parse(sd)
    elif isinstance(sd, float):
        raise StardateError("Float stardate given but not in astronomical mode.")

    year = sd.year
    ordinal = sd.ordinal_day

    days_in_year = 366 if is_leap_year(year) else 365

    if leap_mode == "gregorian":
        if not (1 <= ordinal <= days_in_year):
            raise StardateError("Ordinal out of range for Gregorian")
        real_ordinal = ordinal

    elif leap_mode == "no_leap":
        if not (1 <= ordinal <= 365):
            raise StardateError("Ordinal must be 1..365 in no_leap mode")

        if is_leap_year(year) and ordinal > 59:
            real_ordinal = ordinal + 1
        else:
            real_ordinal = ordinal

        if real_ordinal > days_in_year:
            raise StardateError("Real ordinal exceeds year length")

    else:
        raise StardateError(f"Unknown leap_mode: {leap_mode}")

    return date(year, 1, 1) + timedelta(days = real_ordinal - 1)


def stardate_to_earth_astronomical(sd: float) -> date:
    """
    Convert astronomical fractional stardate back to Earth date.
    """
    year = int(sd)
    fraction = sd - year
    doy = int(round(fraction * 365.2425))

    if doy < 1:
        doy = 1

    return date(year, 1, 1) + timedelta(days = doy - 1)