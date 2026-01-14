# main.py
# kelvin_stardate_cli.py (v1.5-)

import argparse
from datetime import date

from colorama import init as colorama_init

from src.kelvin_stardate.core import (
    earth_to_stardate,
    stardate_to_earth,
    earth_to_stardate_astronomical,
    stardate_to_earth_astronomical,
    is_leap_year,
    StardateError,
)
from src.kelvin_stardate.cli.prompts import (
    ContinuePrompt,
    check_user_input,
    parse_year,
    parse_year_yyyy,
    parse_month,
    parse_day,
    parse_earth_date,
    validate_stardate_string,
    validate_kelvin_stardate_string,
    prompt_until_valid,
    prompt_menu_choice,
    prompt_yes_no,
)
from src.kelvin_stardate.errors import StardateCLIError
from src.kelvin_stardate.cli.helptext import help_loop
from src.kelvin_stardate.cli.colors import COLORS, c, reset


# For header output width
# Note: fits when screen separated in half (so, terminal on
# one side and IDE/VENV on the other)
RESULT_WIDTH = 62 


# ============================================================
# MODE NORMALIZER
# ============================================================

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
    raise StardateCLIError("E006", f"Unknown mode '{mode}'")


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

# ============================================================
# RESULT PRINTER (Unified print block for single-mode)
# ============================================================
def print_single_result(label: str, earth_date=None, stardate=None, input_earth=None, input_sd=None):
    color = COLORS.get(label.lower(), c("header"))

    title = f"RESULT ({label.upper()})"
    border = "=" * RESULT_WIDTH

    print(f"\n {border}")
    print(f" {color}{title.center(RESULT_WIDTH)}{reset()}")
    print(f" {border}")

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

    print(f" {border}\n")


# ============================================================
# EARTH --> STARDATE WRAPPER
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

        title = "RESULTS (ALL MODES)"
        border = "=" * RESULT_WIDTH

        print(f"\n {border}")
        print(f" {c('all')}{title.center(RESULT_WIDTH)}{reset()}")
        print(f" {border}")

        # Show input Earth date at top
        print(f"   {c('label')}Earth date{reset()}          :  {dt}  ({dt.strftime('%B %d, %Y')})\n")

        # Individual mode outputs
        print(f"   {c('no_leap')}Kelvin (no_leap){reset()}    :  {sd_nl}")
        print(f"   {c('gregorian')}Kelvin (gregorian){reset()}  :  {sd_gr}")
        print(f"   {c('astronomical')}Astronomical{reset()}        :  {sd_astr}")

        print(f" {border}\n")
        return

    # ---- SINGLE MODE ----
    if mode == "astronomical":
        sd = earth_to_stardate_astronomical(dt)
        print_single_result("astronomical", stardate=sd, input_earth=dt)
    else:
        sd = earth_to_stardate(dt, mode)
        print_single_result(mode, stardate=sd, input_earth=dt)


# ============================================================
# STARDATE --> EARTH WRAPPER (CLI & INTERACTIVE)
# ============================================================

def do_stardate_to_earth(sd_str, mode):
    # --- Decimals and validation ---
    sd_str = validate_stardate_string(sd_str)

    # ---- ALL MODE ----
    if mode == "all":
        
        title = "RESULTS (ALL MODES)"
        border = "=" * RESULT_WIDTH

        print(f"\n {border}")
        print(f" {c('all')}{title.center(RESULT_WIDTH)}{reset()}")
        print(f" {border}")

        # Show input stardate
        print(f"   {c('label')}Stardate{reset()}            :  {sd_str}\n")

        # no_leap
        try:
            dt_nl = stardate_to_earth(sd_str, "no_leap")
            print(f"   {c('no_leap')}Kelvin (no_leap){reset()}    :  "
                  f"{dt_nl}  ({dt_nl.strftime('%B %d, %Y')})")
        except (StardateError, ValueError, OverflowError):
            print(f"   {c('error')}Kelvin (no_leap): ERROR{reset()}")

        # gregorian
        try:
            dt_gr = stardate_to_earth(sd_str, "gregorian")
            print(f"   {c('gregorian')}Kelvin (gregorian){reset()}  :  "
                  f"{dt_gr}  ({dt_gr.strftime('%B %d, %Y')})")
        except (StardateError, ValueError, OverflowError):
            print(f"   {c('error')}Kelvin (gregorian): ERROR{reset()}")

        # astronomical
        try:
            dt_astr = stardate_to_earth_astronomical(float(sd_str))
            print(f"   {c('astronomical')}Astronomical{reset()}        :  "
                  f"{dt_astr}  ({dt_astr.strftime('%B %d, %Y')})")
        except (ValueError, StardateError, StardateCLIError, OverflowError):
            print(f"   {c('error')}Astronomical: ERROR{reset()}")

        print(f" {border}\n")
        return

    # --- SINGLE MODE ---
    auto = detect_stardate_type(sd_str)

    try:
        if mode == "astronomical" or auto == "astronomical":
            dt = stardate_to_earth_astronomical(float(sd_str))
            print_single_result("astronomical", earth_date=dt, input_sd=sd_str)
        else:
            dt = stardate_to_earth(sd_str, mode)
            print_single_result(mode, earth_date=dt, input_sd=sd_str)

    except OverflowError:
        raise StardateCLIError(
            "E011",
            f"Stardate '{sd_str}' is out of supported range (year must be 0001–9999)."
        )



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
    earth_to.add_argument("month", type=str, help="Month number (1–12) or name/abbreviation (e.g., January)")
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

    def print_cli_error(e: StardateCLIError):
        print(f"{c('error')}Error [{e.code}]: {e.msg}{reset()}")

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║        KELVIN TIMELINE STARDATE CONVERTER (v1.5)         ║")
    print("║        Based on Roberto Orci’s ordinal-date system       ║")
    print("║        Type 'h' for help – 'q' to quit                   ║")
    print("╚══════════════════════════════════════════════════════════╝")

    while True:
        # --------------------------------------------
        # Choose conversion direction
        # --------------------------------------------
        print("\n Conversion Modes:")
        print("   1) Earth → Stardate")
        print("   2) Stardate → Earth")
        print("------------------------------------------------------------")

        mode_choice = prompt_menu_choice(
            " Select an option: ",
            ("1", "2"),
            help_cb=help_loop,
            error_printer=print_cli_error,
        )

        # --------------------------------------------
        # Choose leap/fraction mode (with default)
        # --------------------------------------------
        print("\n Leap Year / Fractional Mode:")
        print(f"   1) {c('no_leap')}no_leap{reset()}       (Orci-style 1..365)")
        print(f"   2) {c('gregorian')}gregorian{reset()}     (true leap-year handling)")
        print(f"   3) {c('astronomical')}astronomical{reset()}  (365.2425 day year)")
        print(f"   4) {c('all')}all{reset()}           (display all modes)")
        print("------------------------------------------------------------")

        # Allows empty input here for default selection.
        # prompt_until_valid() currently disallows empty via check_user_input.
        while True:
            try:
                raw = input(" Choose mode [default=1]: ")

                # Default selection on empty
                if raw.strip() == "":
                    mode = "no_leap"
                    break

                # Normal help/quit + validation path
                check_user_input(raw, help_cb=help_loop)
                mode = normalize_mode(raw)
                break

            except ContinuePrompt:
                # help printed; re-prompt
                continue
            except StardateCLIError as e:
                print_cli_error(e)

        print(f"\n Using mode: {c(mode)}{mode}{reset()}\n")

        # --------------------------------------------
        # Gather inputs + perform conversion
        # --------------------------------------------
        try:
            if mode_choice == "1":
                # Earth -> Stardate
                print(" Enter Earth date components:")
                y = prompt_until_valid(
                    "   Year  (YYYY): ",
                    parse_year_yyyy,
                    help_cb=help_loop,
                    error_printer=print_cli_error,
                )
                m = prompt_until_valid(
                    "   Month (1-12 or name): ",
                    parse_month,
                    help_cb=help_loop,
                    error_printer=print_cli_error,
                )
                d = prompt_until_valid(
                    "   Day   (1-31): ",
                    parse_day,
                    help_cb=help_loop,
                    error_printer=print_cli_error,
                )

                do_earth_to_stardate(y, m, d, mode)

            else:
                # Stardate -> Earth
                if mode in ("astronomical"):
                    validator = validate_stardate_string
                else:
                    validator = validate_kelvin_stardate_string


                sd = prompt_until_valid(
                    " Enter stardate (e.g., 2258.042): ",
                    validator,
                    help_cb=help_loop,
                    error_printer=print_cli_error,
                )

                do_stardate_to_earth(sd, mode)

        except StardateCLIError as e:
            print_cli_error(e)
            continue
        except StardateError as e:
            print(f"{c('error')}Error: {e}{reset()}\n")
            continue

        # --------------------------------------------
        # Replay?
        # --------------------------------------------
        again = prompt_yes_no(
            " Convert another? (y/n): ",
            help_cb=help_loop,
            error_printer=print_cli_error,
        )
        if not again:
            print(f"\n{c('info')}Goodbye!{reset()}\n")
            break



# ============================================================
# MAIN ENTRY
# ============================================================

def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    try:
        # --- Subcommand mode ---
        if args.command == "earth-to":
            mode = normalize_mode(args.mode)
            y, m, d = parse_earth_date(
                f"{args.year}-{args.month}-{args.day}",
                is_leap_year_fn=is_leap_year
            )
            do_earth_to_stardate(y, m, d, mode)
            return

        if args.command == "sd-to":
            mode = normalize_mode(args.mode)
            do_stardate_to_earth(args.stardate, mode)
            return

        # --- Flag-only mode ---
        if args.from_earth:
            y, m, d = parse_earth_date(args.from_earth, is_leap_year_fn=is_leap_year)
            mode = normalize_mode(args.mode)
            do_earth_to_stardate(y, m, d, mode)
            return

        if args.from_sd:
            mode = normalize_mode(args.mode)
            do_stardate_to_earth(args.from_sd, mode)
            return

        # Otherwise interactive fallback
        interactive_menu()

    except StardateCLIError as e:
        print(f"{c('error')}Error [{e.code}]: {e.msg}{reset()}")
        raise SystemExit(2)

    except StardateError as e:
        # Library-level errors (bad ordinals, etc.)
        print(f"{c('error')}Error: {e}{reset()}")
        raise SystemExit(2)


if __name__ == "__main__":
    colorama_init(autoreset=True)
    main()
