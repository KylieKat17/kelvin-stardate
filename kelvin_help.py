# kelvin_help.py

"""
Rich, interactive help system for the Kelvin Timeline Stardate converter.

Provides:
  - ContinuePrompt: control-flow exception used by the CLI
  - help_loop(): interactive help menu used by kelvin_stardate_cli.py
  - show_help_menu(): alias for help_loop()

This module is intentionally CLI-focused: no conversion logic lives here.
"""

from kelvin_errors import (
    list_error_codes_ordered,
    format_error_for_help,
    StardateCLIError,
)

# Initialize color support
from kelvin_colors import c, reset


class ContinuePrompt(Exception):
    """
    Raised when the user requests help inside an input prompt and the CLI
    should re-ask the question afterwards. The CLI catches this and continues.
    """
    pass


# ============================================================
# Shared formatting helpers (no leading underscores)
# ============================================================

def print_banner(title: str):
    """Print a centered banner block with a title."""
    line = "═" * 58
    print()
    print(f"╔{line}╗")
    print(f"║{title.center(58)}║")
    print(f"╚{line}╝")
    print()


def print_section_title(title: str):
    print(f"\n{c('info')}== {title} =={reset()}\n")


def press_enter_or_quit():
    """
    Standard prompt to continue or quit from within help.

    If the user types q/quit/exit, we terminate the entire program
    (mirroring CLI 'quit at any time' behavior).
    """
    text = input(
        f"\n{c('label')}[Press Enter to return to the help menu, or 'q' to quit]{reset()} "
    ).strip().lower()

    if text in ("-q", "q", "/q", "quit", "exit"):
        print(f"\n{c('info')}Goodbye!{reset()}\n")
        raise SystemExit


# ============================================================
# Help sections
# ============================================================

def show_overview():
    print_section_title("Overview")

    print(
        "This tool converts between Earth dates and the Kelvin timeline stardates\n"
        "seen in the J.J. Abrams Star Trek films. The conversion system is based on\n"
        "statements by co-writer Roberto Orci, who described stardates as:\n\n"
        "  • The standard year (e.g. 2258), plus a decimal representing the\n"
        "    fraction of the year / ordinal day within that year.\n\n"
        "For example, in (Kelvin) canon:\n"
        "  • Spock logs the destruction of Vulcan on stardate 2258.42.\n"
        "  • Star Trek Into Darkness begins on stardate 2259.55.\n"
        "  • Star Trek Beyond begins on stardate 2263.02.\n\n"
        "This converter uses Earth dates in ISO-like form, e.g. 2258-02-11, and also\n"
        "prints them in a US-style 'Month DD, YYYY' format for readability.\n\n"
        "Because the films and Orci's explanations are not 100% mathematically\n"
        "rigid, this tool supports several 'modes' for interpreting the decimal:\n"
        "  - A 365-day simplified year (no_leap)\n"
        "  - A real Gregorian leap-year calendar (gregorian)\n"
        "  - A purely fractional 365.2425-day year (astronomical)\n\n"
        "There is also limited auto-detection when converting FROM a stardate:\n"
        "  • Short fractions (e.g. 2258.42) are assumed to be Kelvin-style day\n"
        "    fractions.\n"
        "  • Longer fractional precision (e.g. 2258.11499) helps identify values\n"
        "    produced in astronomical mode.\n"
    )


def show_modes_help():
    print_section_title("Conversion Modes")

    print(
        "The converter supports multiple ways to interpret the fractional part\n"
        "of a Kelvin stardate. You can select these via the interactive menu, the\n"
        "--mode flag, or subcommand options.\n\n"
        "Each mode exists to address a slightly different way of thinking about\n"
        "time in the Kelvin timeline and how strict you want to be about calendar\n"
        "rules and physical year length.\n"
    )

    print(
        f"{c('no_leap')}no_leap{reset()}  "
        "(aliases: 'noleap', 'nl', '1')\n"
        "  • Uses a 365-day year and ignores leap years entirely.\n"
        "  • This roughly matches Orci's simplified \"day of year\" description,\n"
        "    where every year effectively has days 1..365.\n"
        "  • February 29 is compressed so that dates after it don't get shifted.\n"
    )

    print(
        f"{c('gregorian')}gregorian{reset()}  "
        "(aliases: 'greg', 'gr', '2')\n"
        "  • Uses real-world Gregorian calendar rules:\n"
        "      - divisible by 4   ⇒ leap year\n"
        "      - divisible by 100 ⇒ NOT a leap year\n"
        "      - divisible by 400 ⇒ leap year again\n"
        "  • February 29 exists only in true leap years.\n"
        "  • This is the most faithful to how Earth calendars actually behave and\n"
        "    is often useful when reconciling dates against known canon events.\n"
    )

    print(
        f"{c('astronomical')}astronomical{reset()}  "
        "(aliases: 'astro', 'astr', '3')\n"
        "  • Uses a mean tropical year length of 365.2425 days.\n"
        "  • Treats the decimal as a continuous fraction of the year in pure\n"
        "    mathematical terms, without special rules for leap years.\n"
        "  • This is appealing if you want a very smooth, physics/astronomy-leaning\n"
        "    progression of time, even if it diverges slightly from the films.\n"
    )

    print(
        f"{c('all')}all{reset()}  "
        "(aliases: 'a', '4')\n"
        "  • Computes and displays conversions under all three modes at once.\n"
        "  • This is especially helpful when you're trying to decide which mode\n"
        "    best matches a given interpretation of Kelvin canon.\n"
    )

    print(
        "\nWhy not Julian or other calendars?\n"
        "  • The Kelvin films implicitly assume a Gregorian-flavored context, and\n"
        "    Orci's explanations are conceptually closest to an ordinal-date view\n"
        "    of Earth years. Julian calendars or other more obscure systems would\n"
        "    add historical complexity without improving the match to on-screen\n"
        "    stardates, so they were deliberately not included.\n"
    )


def show_error_codes_help(dev_mode: bool = False):
    print_section_title("Error Codes")

    print(
        "When something goes wrong, the CLI may report a structured error in\n"
        "the form:  Error [EXXX]: message\n\n"
        "The EXXX codes make it easier to understand and look up what failed.\n"
        "Here are the currently defined codes:\n"
    )

    for info in list_error_codes_ordered():
        text = format_error_for_help(info.code, dev_mode=dev_mode)
        print(f"  {c('label')}{text}{reset()}\n")

    print(
        "If you see an error code not listed here, it may be newly added in\n"
        "kelvin_errors.ERROR_REGISTRY. You can extend this help view by updating\n"
        "kelvin_help.show_error_codes_help or relying on format_error_for_help.\n"
    )


def show_usage_help():
    print_section_title("Usage (Interactive, Flags, Subcommands)")

    print(
        f"{c('success')}1) Interactive mode{reset()}\n"
        "   Run with no arguments:\n"
        "       python .\kelvin_stardate_cli.py\n\n"
        "   You'll see a menu:\n"
        "       1) Earth → Stardate\n"
        "       2) Stardate → Earth\n\n"
        "   At ANY prompt in the interactive UI you can type:\n"
        "       q, /q, quit, exit   → quit the program\n"
        "       h, /h, help, /help  → open this help menu\n\n"
        "   Month input is flexible:\n"
        "       '1', '01', 'jan', 'january' → all treated as January.\n"
    )

    print(
        f"{c('success')}2) Flag-style usage{reset()}\n"
        "   Earth → Stardate:\n"
        "       python kelvin_stardate_cli.py --from-earth 2258-02-11 --mode all\n\n"
        "   Stardate → Earth:\n"
        "       python kelvin_stardate_cli.py --from-sd 2258.42 --mode greg\n\n"
        "   Mode strings support full names and abbreviations:\n"
        "       no_leap, noleap, nl, 1\n"
        "       gregorian, greg, gr, 2\n"
        "       astronomical, astro, astr, 3\n"
        "       all, a, 4\n"
    )

    print(
        f"{c('success')}3) Subcommands{reset()}\n"
        "   Earth → Stardate:\n"
        "       python kelvin_stardate_cli.py earth-to 2258 2 11 --mode all\n\n"
        "   Stardate → Earth:\n"
        "       python kelvin_stardate_cli.py sd-to 2258.42 --mode gregorian\n\n"
        "   Subcommands are useful if you prefer positional arguments or want to\n"
        "   script things more explicitly.\n"
    )


def show_examples_help():
    print_section_title("Examples")

    print(
        f"{c('success')}Example 1 – Earth → Stardate (ALL modes){reset()}\n"
        "   Input:\n"
        "       python kelvin_stardate_cli.py earth-to 2258 2 11 --mode all\n\n"
        "   Output (shape):\n"
        "       ====================== RESULTS (ALL MODES) ======================\n"
        "         Earth date         :  2258-02-11  (February 11, 2258)\n"
        "\n"
        "         Kelvin (no_leap)   :  2258.42\n"
        "         Kelvin (gregorian) :  2258.42\n"
        "         Astronomical       :  2258.11499\n"
        "       =================================================================\n"
    )

    print(
        f"{c('success')}Example 2 – Stardate → Earth (gregorian){reset()}\n"
        "   Input:\n"
        "       python kelvin_stardate_cli.py sd-to 2258.42 --mode greg\n\n"
        "   Output (shape):\n"
        "       ====================== RESULT (GREGORIAN) ======================\n"
        "         Stardate     :  2258.42\n"
        "         Earth date   :  2258-02-11  (February 11, 2258)\n"
        "       =================================================================\n"
    )

    print(
        f"{c('success')}Example 3 – Interactive, with help and quit{reset()}\n"
        "   • Run:\n"
        "       python kelvin_stardate_cli.py\n"
        "   • Use 'h' or '/help' at any prompt for this help system.\n"
        "   • Use 'q' or 'quit' at any prompt to exit immediately.\n"
    )


def show_troubleshooting_help():
    print_section_title("Troubleshooting & Common Issues")

    print(
        f"{c('label')}Problem:{reset()} Month or date rejected (E002 / E003).\n"
        "  → Month may be outside 1–12, or the name may be unrecognized.\n"
        "    Day might be outside 1–31, or invalid for that month and year.\n\n"
        f"{c('label')}Problem:{reset()} Leap day issues (E004).\n"
        "  → You used February 29 on a year that is not a leap year in the\n"
        "    Gregorian calendar.\n\n"
        f"{c('label')}Problem:{reset()} Stardate format error (E005).\n"
        "  → Kelvin-style stardates must include a decimal fraction, e.g. 2258.42.\n"
        "    A bare '2258' is not considered valid for conversion.\n\n"
        f"{c('label')}Problem:{reset()} Empty input (E001).\n"
        "  → The program expected a value but you just pressed Enter.\n\n"
        f"{c('label')}Problem:{reset()} Unknown mode (E006).\n"
        "  → Your --mode or menu choice could not be mapped to a known mode.\n"
        "    Try one of: no_leap, gregorian, astronomical, all, or their aliases.\n"
    )


def show_all_topics(dev_mode: bool = False):
    """
    Dump all core help sections in one go. This is invoked when the user picks
    the 'All' option from the help menu (or presses 'a').
    """
    print_banner("FULL HELP (ALL TOPICS)")

    show_overview()
    show_modes_help()
    show_error_codes_help(dev_mode=dev_mode)
    show_usage_help()
    show_examples_help()
    show_troubleshooting_help()

    press_enter_or_quit()


# ============================================================
# Top-level interactive help loop
# ============================================================

def help_loop():
    """
    Interactive help menu. Called from the CLI when the user types 'h',
    '/h', 'help', or '/help'.

    Returns normally when the user chooses to go back; the caller typically
    catches ContinuePrompt to re-ask whatever question they were on.
    """
    while True:
        print_banner("KELVIN STARDATE HELP")

        print("   1) Overview")
        print("   2) Conversion Modes")
        print("   3) Error Codes")
        print("   4) Usage (interactive, flags, subcommands)")
        print("   5) Examples")
        print("   6) Troubleshooting / Common Issues")
        print("   7) All topics (full help dump)")
        print("   8) Return to previous prompt")
        print("------------------------------------------------------------")

        choice = input(" Select a help topic (1-8, or letter): ").strip().lower()

        # Quit-at-any-time behavior inside help
        if choice in ("q", "/q", "quit", "exit"):
            print(f"\n{c('info')}Goodbye!{reset()}\n")
            raise SystemExit

        
        # All topics
        if choice in ("7", "a", "all"):
            show_all_topics(dev_mode=False)
            continue

        # Return to the calling prompt
        if choice in ("8", "", "r", "back", "b"):
            return

        # Route by number or first-letter mnemonic
        if choice in ("1", "o", "overview"):
            show_overview()
            press_enter_or_quit()
        elif choice in ("2", "m", "mode", "modes"):
            show_modes_help()
            press_enter_or_quit()
        elif choice in ("3", "e", "err", "errors", "codes"):
            show_error_codes_help(dev_mode=False)
            press_enter_or_quit()
        elif choice in ("4", "u", "usage"):
            show_usage_help()
            press_enter_or_quit()
        elif choice in ("5", "x", "ex", "example", "examples"):
            show_examples_help()
            press_enter_or_quit()
        elif choice in ("6", "t", "trouble", "troubleshooting"):
            show_troubleshooting_help()
            press_enter_or_quit()
        else:
            print(f"{c('error')} Unrecognized choice. Please select 1–8 or a matching letter.{reset()}")
            press_enter_or_quit()


def show_help_menu():
    """Thin alias retained for any existing imports."""
    help_loop()
