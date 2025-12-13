# kelvin_stardate_cli.py

from datetime import date
from kelvin_stardate import (
    earth_to_stardate,
    stardate_to_earth,
    earth_to_stardate_astronomical,
    stardate_to_earth_astronomical,
    StardateError
)
from colorama import Fore, Style, init

init(autoreset=True)

def check_quit(value: str):
    """Exit program if user types 'q' at any prompt."""
    if value.strip().lower() == "q":
        print("\nGoodbye!\n")
        raise SystemExit


def choose_leap_mode():
    print("\nLeap year handling:")
    print("  1. 'no_leap'       (Orci-style 1..365)")
    print("  2. 'gregorian'     (true 1..365/366)")
    print("  3. 'astronomical'  (fractional 365.2425)")
    print("  4. 'all'           (show all three)")
    choice = input("Choose (1/2/3/4) [default 1]: ").strip()

    if choice == "2":
        return "gregorian"
    if choice == "3":
        return "astronomical"
    if choice == "4":
        return "all"
    return "no_leap"

def detect_stardate_type(sd_str: str):
    """
    Auto-detect whether input is Kelvin or Astronomical:
        Kelvin: decimal portion 1–3 digits
        Astronomical: 4+ digits OR floats like 2258.11342
    """
    try:
        year, frac = sd_str.split(".", 1)
    except ValueError:
        return "kelvin"  # something like "2258"—Kelvin-like, will error if invalid

    if not frac.isdigit():
        return "kelvin"

    if len(frac) >= 4:
        return "astronomical"

    return "kelvin"


def main():
    print("=== Kelvin Timeline Stardate Converter ===")
    print("Based on Roberto Orci's ordinal date system.")
    print("Type 'q' at ANY prompt to quit.\n")

    while True:
        print("1. Earth → Stardate")
        print("2. Stardate → Earth")
        mode_choice = input("Choose (1 or 2): ").strip()
        check_quit(mode_choice)

        leap_mode = choose_leap_mode()
        print(f"\nUsing leap_mode: {leap_mode}\n")

        try:
            #
            # -----------------------------------------
            # EARTH → STARDATE
            # -----------------------------------------
            #
            if mode_choice == "1":
                y = input("Year: ")
                check_quit(y)
                m = input("Month: ")
                check_quit(m)
                d = input("Day: ")
                check_quit(d)

                dt = date(int(y), int(m), int(d))

                if leap_mode == "all":
                    sd_nl = earth_to_stardate(dt, "no_leap")
                    sd_gr = earth_to_stardate(dt, "gregorian")
                    sd_ast = earth_to_stardate_astronomical(dt)

                    print("\n--- RESULTS (ALL MODES) ---")
                    print(f"{Fore.CYAN}Kelvin (no_leap):     {sd_nl}")
                    print(f"{Fore.CYAN}Kelvin (gregorian):   {sd_gr}")
                    print(f"{Fore.GREEN}Astronomical:         {sd_ast}{Style.RESET_ALL}")
                    print()

                else:
                    if leap_mode == "astronomical":
                        sd = earth_to_stardate_astronomical(dt)
                        print(f"\n{Fore.GREEN}Stardate (astronomical): {sd}{Style.RESET_ALL}\n")
                    else:
                        sd = earth_to_stardate(dt, leap_mode)
                        print(f"\n{Fore.CYAN}Stardate (Kelvin):       {sd}{Style.RESET_ALL}\n")

            #
            # -----------------------------------------
            # STARDATE → EARTH
            # -----------------------------------------
            #
            elif mode_choice == "2":
                sd_str = input("Enter stardate: ").strip()
                check_quit(sd_str)

                if leap_mode == "all":
                    print("\n--- RESULTS (ALL MODES) ---")

                    # Kelvin no_leap
                    try:
                        dt_nl = stardate_to_earth(sd_str, "no_leap")
                        print(f"{Fore.CYAN}Kelvin (no_leap):     {dt_nl}  ({dt_nl.strftime('%B %d, %Y')})")
                    except Exception:
                        print(f"{Fore.RED}Kelvin (no_leap):     ERROR")

                    # Kelvin gregorian
                    try:
                        dt_gr = stardate_to_earth(sd_str, "gregorian")
                        print(f"{Fore.CYAN}Kelvin (gregorian):   {dt_gr}  ({dt_gr.strftime('%B %d, %Y')})")
                    except Exception:
                        print(f"{Fore.RED}Kelvin (gregorian):   ERROR")

                    # Astronomical
                    try:
                        sd_float = float(sd_str)
                        dt_ast = stardate_to_earth_astronomical(sd_float)
                        print(f"{Fore.GREEN}Astronomical:         {dt_ast}  ({dt_ast.strftime('%B %d, %Y')})")
                    except Exception:
                        print(f"{Fore.RED}Astronomical:         ERROR")

                    print()

                else:
                    # AUTO-DETECTION APPLIES HERE
                    auto = detect_stardate_type(sd_str)

                    # Single-mode execution
                    if leap_mode == "astronomical" or auto == "astronomical":
                        try:
                            sd_float = float(sd_str)
                        except ValueError:
                            raise StardateError("Input must be a float for astronomical mode.")
                        dt = stardate_to_earth_astronomical(sd_float)
                    else:
                        dt = stardate_to_earth(sd_str, leap_mode)

                    print(f"\nEarth date: {dt}  ({dt.strftime('%B %d, %Y')})\n")

            else:
                print(f"{Fore.RED}Invalid choice.\n")

        except Exception as e:
            print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}\n")

        #
        # ALWAYS ask whether to convert again
        #
        again = input("Convert another? (y/n): ")
        check_quit(again)
        if again.strip().lower() != "y":
            print("\nGoodbye!\n")
            break


if __name__ == "__main__":
    main()