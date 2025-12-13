from datetime import date, timedelta


# -----------------------------
#   SUPPORT UTILITIES
# -----------------------------
def day_of_year(dt: date) -> int:
    """Return the 1-based day of year from a date."""
    return (dt - date(dt.year, 1, 1)).days + 1


def format_stardate(sd: float, precision=2) -> str:
    """Format stardate with a fixed decimal precision."""
    return f"{sd:.{precision}f}"


# -----------------------------
#   OPTION A — ASTRONOMICAL
# -----------------------------
def earth_to_stardate_A(dt: date, tropical_year=365.2425) -> float:
    """Stardate = YEAR + (day_of_year / 365.2425)"""
    doy = day_of_year(dt)
    return dt.year + (doy / tropical_year)


def stardate_to_earth_A(sd: float, tropical_year=365.2425) -> date:
    """Inverse: YEAR + fraction*365.2425"""
    year = int(sd)
    fraction = sd - year
    day_float = fraction * tropical_year
    day_num = int(day_float) or 1
    return date(year, 1, 1) + timedelta(days=day_num - 1)


# -----------------------------
#   OPTION B — ORCI CANON
# -----------------------------
def earth_to_stardate_B(dt: date, use_leap=False) -> float:
    """
    Stardate = YEAR + (DAY_OF_YEAR / 365)
    Orci did NOT specify leap-year handling, so 365 is correct.
    """
    doy = day_of_year(dt)
    year_length = 366 if use_leap else 365
    return dt.year + (doy / year_length)


def stardate_to_earth_B(sd: float, use_leap=False) -> date:
    """Inverse for canonical Orci rule."""
    year = int(sd)
    fraction = sd - year
    year_length = 366 if use_leap else 365
    day_float = fraction * year_length
    day_num = int(day_float) or 1
    return date(year, 1, 1) + timedelta(days=day_num - 1)


# -----------------------------
#   CLI
# -----------------------------
def main():
    print("=== Kelvin Stardate Converter (Canon Orci System) ===")
    print("1. Earth → Stardate")
    print("2. Stardate → Earth")
    choice = input("Choose (1 or 2): ")

    if choice == "1":
        year = int(input("Year: "))
        month = int(input("Month: "))
        day = int(input("Day: "))
        dt = date(year, month, day)

        leap = input("Use leap-year mode? (y/n): ").lower().startswith("y")
        precision = int(input("Decimal precision for output (2 recommended): "))

        sdA = earth_to_stardate_A(dt)
        sdB = earth_to_stardate_B(dt, use_leap=leap)

        print("\n--- Results ---")
        print("Option A (Astronomical):", format_stardate(sdA, precision))
        print("Option B (Canonical Orci):", format_stardate(sdB, precision))

    elif choice == "2":
        sd = float(input("Stardate (e.g., 2258.42): "))
        leap = input("Use leap-year mode? (y/n): ").lower().startswith("y")

        dtA = stardate_to_earth_A(sd)
        dtB = stardate_to_earth_B(sd, use_leap=leap)

        print("\n--- Results ---")
        print("Option A (Astronomical):", dtA)
        print("Option B (Canonical Orci):", dtB)

    else:
        print("Invalid selection.")

