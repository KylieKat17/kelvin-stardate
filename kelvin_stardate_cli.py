# kelvin_stardate_cli.py

import argparse
from datetime import date

#
from kelvin_stardate import (
    earth_to_stardate,
    stardate_to_earth,
    earth_to_stardate_astronomical,
    stardate_to_earth_astronomical,
    StardateError,
)

from kelvin_errors import StardateCLIError
from kelvin_help import help_loop

from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# ============================================================
# GLOBAL COLORS (Softer, readable color palette for PowerShell Dark Mode)
# ============================================================
MODE_COLORS = {
    "all": Fore.LIGHTYELLOW_EX,
    "no_leap": Fore.LIGHTBLUE_EX,
    "gregorian": Fore.LIGHTCYAN_EX,
    "astronomical": Fore.LIGHTGREEN_EX,
}

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
# CONTROL EXCEPTION (help-trigger re-prompt)
# ============================================================

class ContinuePrompt(Exception):
    """Raised after help is shown to restart the prompt."""
    pass

# TODO: ADD RED ERROR STYLING WHERE NECESSARY
# ============================================================
# HELP + QUIT + EMPTY HANDLER
# ============================================================

def check_user_input(value: str):
    """Resolves q/quit + help/h and empty errors."""
    if value is None:
        raise StardateCLIError("E007", "Empty input.")

    stripped = value.strip().lower()

    # Quit
    if stripped in ("q", "/q", "quit", "exit"):
        print(f"\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}\n")
        raise SystemExit

    # Help
    if stripped in ("h", "/h", "help", "/help"):
        help_loop()
        raise ContinuePrompt

    # Empty string
    if stripped == "":
        raise StardateCLIError("E007", "Input cannot be empty.")

    return value

# ============================================================
# MONTH + DAY PARSERS
# ============================================================

def parse_month(value: str) -> int:
    check_user_input(value)
    raw_month_v = value.strip().lower()

    if raw_month_v in MONTH_LOOKUP:
        return MONTH_LOOKUP[raw_month_v]

    if raw_month_v.isdigit():
        m = int(raw_month_v)
        if 1 <= m <= 12:
            return m
        raise StardateCLIError("E001", f"Invalid numeric month '{raw_month_v}'")

    raise StardateCLIError("E001", f"Unrecognized month '{value}'")


def parse_day(value: str) -> int:
    check_user_input(value)
    raw_day_v = value.strip()

    if not raw_day_v.isdigit():
        raise StardateCLIError("E002", f"Invalid day '{value}'")

    d = int(raw_day_v)
    if not (1 <= d <= 31):
        raise StardateCLIError("E002", f"Day '{d}' out of range 1–31")

    return d

# ============================================================
# LEAP YEAR CHECK
# ============================================================
def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


# ============================================================
# MODE NORMALIZER
# ============================================================

#def normalize_mode(mode: str):
def normalize_mode(mode):
    mode = mode.lower().strip()
    if mode in ("1", "no_leap", "noleap", "nl", "canon", "ordinal"):
        return "no_leap"
    if mode in ("2", "gregorian", "greg", "gr"):
        return "gregorian"
    if mode in ("3", "astronomical", "astro", "astr"):
        return "astronomical"
    if mode in ("4", "all", "a"):
        return "all"
    raise StardateCLIError("E008", f"Unknown mode '{mode}'")


# ============================================================
# AUTO-DETECT STARDATE TYPE (kelvin vs astronomical)
# ============================================================

def detect_stardate_type(sd: str):
    try:
        whole, frac = sd.split(".", 1)
    except ValueError:
        return "kelvin"

    if not frac.isdigit():
        return "kelvin"

    return "astronomical" if len(frac) >= 4 else "kelvin"

# TODO: add redisplay of both earth and stardate on output ??? CHECK IF IMPLEMENTED
# ============================================================
# RESULT PRINTER (Unified print block for single-mode)
# ============================================================
def print_single_result(label: str, earth_date=None, stardate=None, input_earth=None, input_sd=None):
    color = MODE_COLORS.get(label.lower(), Fore.WHITE)
    # label_upper = label.upper()

    print("\n ====================== ", end="")
    print(f"{color}RESULT ({label.upper()}){Style.RESET_ALL}", end="")
    print(" ======================")

    # Always show input at the top
    if input_earth is not None:
        ie = input_earth
        print(f"   Earth date   :  {ie}  ({ie.strftime('%B %d, %Y')})")

    if input_sd is not None:
        print(f"   Stardate     :  {input_sd}")

    # Then show computed result
    if stardate is not None:
        print(f"   Stardate     :  {stardate}")

    if earth_date is not None:
        print(f"   Earth date   :  {earth_date}  ({earth_date.strftime('%B %d, %Y')})")

    print(" =================================================================\n")


# ============================================================
# EARTH → STARDATE WRAPPER
# ============================================================

def do_earth_to_stardate(y, m, d, mode):
    try:
        dt = date(y, m, d)
    except ValueError:
        raise StardateCLIError("E002", f"Invalid date {y}-{m}-{d}")

    # ---- ALL MODE ----
    if mode == "all":
        sd_nl   = earth_to_stardate(dt, "no_leap")
        sd_gr   = earth_to_stardate(dt, "gregorian")
        sd_astr = earth_to_stardate_astronomical(dt)

        print("\n ====================== ", end="")
        print(f"{MODE_COLORS['all']}RESULTS (ALL MODES){Style.RESET_ALL}", end = "")
        print(" ======================")

        # Show input Earth date at top
        print(f"   {Fore.YELLOW}Earth date{Style.RESET_ALL}          :  {dt}  ({dt.strftime('%B %d, %Y')})\n")

        # Individual mode outputs (cyan for Kelvins, green for astronomical)
        print(f"   {Fore.CYAN}Kelvin (no_leap){Style.RESET_ALL}    :  {sd_nl}")
        print(f"   {Fore.CYAN}Kelvin (gregorian){Style.RESET_ALL}  :  {sd_gr}")
        print(f"   {Fore.GREEN}Astronomical{Style.RESET_ALL}        :  {sd_astr}")

        print(" =================================================================\n")
        return

    # ---- SINGLE MODE ----
    if mode == "astronomical":
        sd = earth_to_stardate_astronomical(dt)
        print_single_result("astronomical", stardate=sd, input_earth=dt)
    else:
        sd = earth_to_stardate(dt, mode)
        print_single_result(mode, stardate=sd, input_earth=dt)


# ============================================================
# STARDATE → EARTH WRAPPER (CLI & INTERACTIVE)
# ============================================================

def do_stardate_to_earth(sd_str, mode):
    if "." not in sd_str:
        raise StardateCLIError("E005", "Stardate must contain a decimal.")

    # ---- ALL MODE ----
    if mode == "all":
        print("\n ====================== ", end="")
        print(f"{MODE_COLORS['all']}RESULTS (ALL MODES){Style.RESET_ALL}", end="")
        print(" ======================")

        # Show input stardate
        print(f"   {Fore.YELLOW}Stardate{Style.RESET_ALL}            :  {sd_str}\n")

        # TODO: ADD ERROR CODES IN ERROR MESSAGES!!!!!!
        # no_leap
        try:
            dt_nl = stardate_to_earth(sd_str, "no_leap")
            print(f"   {Fore.CYAN}Kelvin (no_leap){Style.RESET_ALL}    :  "
                  f"{dt_nl}  ({dt_nl.strftime('%B %d, %Y')})")
        except Exception:
            print(f"   {Fore.RED}Kelvin (no_leap): ERROR{Style.RESET_ALL}")

        # gregorian
        try:
            dt_gr = stardate_to_earth(sd_str, "gregorian")
            print(f"   {Fore.CYAN}Kelvin (gregorian){Style.RESET_ALL}  :  "
                  f"{dt_gr}  ({dt_gr.strftime('%B %d, %Y')})")
        except Exception:
            print(f"   {Fore.RED}Kelvin (gregorian): ERROR{Style.RESET_ALL}")

        # astronomical
        try:
            dt_astr = stardate_to_earth_astronomical(float(sd_str))
            print(f"   {Fore.GREEN}Astronomical{Style.RESET_ALL}        :  "
                  f"{dt_astr}  ({dt_astr.strftime('%B %d, %Y')})")
        except Exception:
            print(f"   {Fore.RED}Astronomical: ERROR{Style.RESET_ALL}")

        print(" =================================================================\n")
        return

    # --- SINGLE MODE ---
    auto = detect_stardate_type(sd_str)
    if mode == "astronomical" or auto == "astronomical":
        dt = stardate_to_earth_astronomical(float(sd_str))
        print_single_result("astronomical", earth_date=dt, input_sd=sd_str)
    else:
        dt = stardate_to_earth(sd_str, mode)
        print_single_result(mode, earth_date=dt, input_sd=sd_str)


# ============================================================
# BUILD ARGPARSE SUBCOMMANDS + FLAGS
# ============================================================

def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Kelvin Timeline Stardate Converter (CLI + Subcommands)",
        add_help=True,
    )

    # ------------------------------
    # Top-level flags
    # ------------------------------
    parser.add_argument(
        "--from-earth", type=str,
        help="Convert Earth date YYYY-MM-DD → stardate (respecting --mode)."
    )
    parser.add_argument(
        "--from-sd", type=str,
        help="Convert stardate → Earth date (respecting --mode)."
    )
    # TODO: MIGHT simplify the help= message. Its a bit big
    parser.add_argument(
        "--mode", type=str, default="no_leap",
        help=(
            "Conversion mode:\n"
            "  no_leap       Orci-style 365-day year\n"
            "  gregorian     Actual leap-year calendar\n"
            "  astronomical  365.2425-day fractional year\n"
            "  all           Display results from all modes\n"
        )
    )

    # ------------------------------
    # Subcommands
    # ------------------------------
    sub = parser.add_subparsers(
        dest="command",
        help="Available subcommands (use `stardate <cmd> --help` for details).",
    )

    # earth-to
    earth_to = sub.add_parser(
        "earth-to",
        help="Convert an Earth date → stardate.",
        description="Convert a calendar Earth date into a Kelvin-format stardate.",
    )
    earth_to.add_argument("year", type=int, help="Year (e.g., 2258)")
    earth_to.add_argument("month", type=int, help="Month number (1–12)")
    earth_to.add_argument("day", type=int, help="Day of the month (1–31)")
    earth_to.add_argument(
        "--mode", type=str, default="no_leap",
        help="Conversion mode (no_leap, gregorian, astronomical, all)."
    )

    # sd-to
    sd_to = sub.add_parser(
        "sd-to",
        help="Convert a stardate → Earth date.",
        description="Convert Kelvin-format stardates back into Earth calendar dates.",
    )
    sd_to.add_argument("stardate", type=str, help="Example: 2258.42")
    sd_to.add_argument(
        "--mode", type=str, default="no_leap",
        help="Conversion mode (no_leap, gregorian, astronomical, all)."
    )

    return parser



# ============================================================
# INTERACTIVE MENU
# ============================================================

def interactive_menu():

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║        KELVIN TIMELINE STARDATE CONVERTER (v1.4)         ║")
    print("║        Based on Roberto Orci’s ordinal-date system       ║")
    print("║        Type 'h' for help – 'q' to quit                   ║")
    print("╚══════════════════════════════════════════════════════════╝\n")

    while True:
        # TODO: add a print something here because it just looks odd in terminal. no clue why it looks odd, it just does
        print("   1) Earth → Stardate")
        print("   2) Stardate → Earth")
        print("------------------------------------------------------------")

        try:
            choice_raw = input(" Select an option: ")
            check_user_input(choice_raw)
            mode_choice = choice_raw.strip()
        except ContinuePrompt:
            continue
        except StardateCLIError as e:
            print(f"{Fore.RED}Error [{e.code}]: {e.msg}{Style.RESET_ALL}\n")
            continue

        # MODE MENU
        print("\n Leap Year / Fractional Mode:")
        print("   1) no_leap       (Orci-style 1..365)")
        print("   2) gregorian     (true leap-year handling)")
        print("   3) astronomical  (365.2425 day year)")
        print("   4) all           (display all modes)")
        print("------------------------------------------------------------")

        try:
            mode_raw = input(" Choose mode [default=1]: ")
            check_user_input(mode_raw)
            mode = normalize_mode(mode_raw or "no_leap")

            # TODO: make it so it displays the correct mode color for what version it uses
            # if not, regular yellow works (Fore.YELLOW). though i would like that to be for "all"
            # CHECK IMPLEMENTATION ON NEW VERSION
            print(f"\n Using mode: {MODE_COLORS[mode]}{mode}{Style.RESET_ALL}\n")
        except ContinuePrompt:
            continue
        except StardateCLIError as e:
            print(f"{Fore.RED}Error [{e.code}]: {e.msg}{Style.RESET_ALL}\n")
            continue

        # SELECTION LOGIC
        # NOTE: I FEEL LIKE YOU CAN CONDENSE THIS 
        try:
            if mode_choice == "1":
                # EARTH → STARDATE
                y_raw = input(" Year: "); check_user_input(y_raw)
                m_raw = input(" Month: "); check_user_input(m_raw)
                d_raw = input(" Day: "); check_user_input(d_raw)

                y = int(y_raw)
                m = parse_month(m_raw)
                d = parse_day(d_raw)

                # Leap-day validation
                if m == 2 and d == 29 and not is_leap_year(y):
                    raise StardateCLIError("E003", f"{y} is not a leap year.")

                do_earth_to_stardate(y, m, d, mode)

            elif mode_choice == "2":
                sd_raw = input(" Enter stardate: ")
                check_user_input(sd_raw)
                do_stardate_to_earth(sd_raw, mode)

            else:
                print(f"{Fore.RED}Invalid selection.{Style.RESET_ALL}")

        except ContinuePrompt:
            continue
        except StardateCLIError as error:
            print(f"{Fore.RED}Error [{error.code}]: {error.msg}{Style.RESET_ALL}\n")
        except Exception as error:
            print(f"{Fore.RED}Unexpected Error: {error}{Style.RESET_ALL}\n")

        # Continue?
        again = input(" Convert another? (y/n): ")
        try:
            check_user_input(again)
        except ContinuePrompt:
            continue

        if again.strip().lower() != "y":
            print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}\n")
            break


# ============================================================
# MAIN ENTRY
# ============================================================

def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    # --- Subcommand mode ---
    if args.command == "earth-to":
        mode = normalize_mode(args.mode)
        do_earth_to_stardate(args.year, args.month, args.day, mode)
        return

    if args.command == "sd-to":
        mode = normalize_mode(args.mode)
        do_stardate_to_earth(args.stardate, mode)
        return

    # --- Flag-only mode ---
    if args.from_earth:
        y, m, d = map(int, args.from_earth.split("-"))
        mode = normalize_mode(args.mode)
        do_earth_to_stardate(y, m, d, mode)
        return

    if args.from_sd:
        mode = normalize_mode(args.mode)
        do_stardate_to_earth(args.from_sd, mode)
        return

    # Otherwise interactive fallback
    interactive_menu()


if __name__ == "__main__":
    main()
