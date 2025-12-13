# kelvin_help.py

from colorama import Fore, Style
from kelvin_errors import ERROR_CODES

HELP_HEADER_COLOR = Fore.LIGHTCYAN_EX
SECTION_COLOR = Fore.LIGHTYELLOW_EX


def print_help_overview():
    print()
    print(HELP_HEADER_COLOR + "════════════════════════════════════════════════════════════")
    print("                    KELVIN STARDATE HELP")
    print("════════════════════════════════════════════════════════════" + Style.RESET_ALL)
    print("""
Available Help Topics:
  1) general       – What the converter does
  2) modes         – no_leap, gregorian, astronomical, all
  3) input         – accepted date formats, month names, stardate formats
  4) errors        – explanation of all error codes
  5) commands      – CLI flags and subcommands
  6) quit          – exits this menu

Enter a help topic (e.g. 'modes', 'errors') or 'quit'.
""")


# TODO: OVERALL UNSORTED THOUGHTS: ADD INFORMATION ABOUT WHAT THE SYSTEM'S VERSION USES (like about Orci, the movies we're pulling from, our sources, and what each kind of calander means, the issues arrising in Kelvin cannon continuity, etc. Like citing ISO standard for earth dates resulting in YYYY-MM-DD and our "Month day, year" format). WHY THESE CONVERSION TYPES WERE USED. THAT THERE IS AUTO-DETECTION FOR TYPE ON STARDATES
def help_general():
    print(SECTION_COLOR + "\nGENERAL INFORMATION" + Style.RESET_ALL)
    print("""
This program converts between:
  • Earth calendar dates (YYYY-MM-DD or components)
  • Kelvin Timeline stardates (J.J. Abrams rule: YYYY.DDD)

Internally, three conversion models are available:
  1. no_leap       – simple 1..365 ordinal (Orci system)
  2. gregorian     – uses true Gregorian leap-year calendar
  3. astronomical  – fractional 365.2425-year
""")

# needs to further explain what the fuck these modes each are, why they were chosen, and why others were not (julian for example)
def help_modes():
    print(SECTION_COLOR + "\nCONVERSION MODES" + Style.RESET_ALL)
    print("""
no_leap:
    Follows Roberto Orci's simplified ordinal numbering where all years
    behave as if they have exactly 365 days.

gregorian:
    Obeys true Gregorian rules:
        divisible by 4 → leap year
        divisible by 100 → NOT a leap year
        divisible by 400 → leap year

astronomical:
    Uses a continuous fractional year length of 365.2425 days.

all:
    Displays all three conversions simultaneously.
""")


def help_input():
    print(SECTION_COLOR + "\nINPUT FORMATS" + Style.RESET_ALL)
    print("""
Valid Earth Months:
    • Numeric: 1, 01, 12
    • Names: january, jan, Feb, SEP, etc.

Valid Earth Days:
    • 1–31 (validated per month/year)

Stardates:
    • Must contain one decimal point: e.g. 2258.42
    • Kelvin type requires 2–3 fractional digits.
    • Astronomical type may use more digits.
""")


def help_errors():
    print(SECTION_COLOR + "\nERROR CODES" + Style.RESET_ALL)
    print("Below are all defined error codes and their meanings:\n")
    for code, description in ERROR_CODES.items():
        print(f"  {Fore.CYAN}{code}{Style.RESET_ALL}  {description}")
    print()

# needs to be updated! it's messy and unclear. also, we've added abbreviations for things like gregorian or astronomical
def help_commands():
    print(SECTION_COLOR + "\nCOMMANDS & FLAGS" + Style.RESET_ALL)
    print("""
Examples:

  stardate earth-to 2258 2 11 --mode gregorian
  stardate sd-to 2258.42 --mode all

  python kelvin_stardate_cli.py --from-earth 2258-02-11
  python kelvin_stardate_cli.py --from-sd 2258.42 --mode astronomical
""")

# ADD AN ALL OPTION SO IT CAN DISPLAY THE FULL MENU IF THE USER DESIRES
# also, modify the accept numbers and q for quit (maybe also e for error, g for general and so on) instead of full type outs. because I keep accidentally inputting numbers. maybe just have it detect the first letter of an input as well and assume from there. So long as we make all the menu options start with different letters.
# OR could potentially do it as a global??
# also, the loop needs to call the desired section and then ask if the user wants to continue in the help menu instead immediately redisplaying the menu
# Same quit at any time logic as well

def help_loop():
    """Interactive help navigation."""
    while True:
        print_help_overview()
        choice = input("Help> ").strip().lower()

        if choice in ("quit", "q"):
            print()
            return
        elif choice == "general":
            help_general()
        elif choice == "modes":
            help_modes()
        elif choice == "input":
            help_input()
        elif choice == "errors":
            help_errors()
        elif choice == "commands":
            help_commands()
        else:
            print(Fore.RED + "Unknown help topic." + Style.RESET_ALL)
