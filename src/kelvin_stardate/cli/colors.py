# colors.py
# kelvin_colors.py (v1.5-)

"""
Centralized color and style definitions for the Kelvin Stardate Converter.
"""

from colorama import Fore, Style

# ============================================================
# Semantic Color Palette
# ============================================================
# These are named for *meaning*, not just hue.

COLORS = {
    # General
    "reset": Style.RESET_ALL,
    "error": Fore.LIGHTRED_EX,
    "warning": Fore.LIGHTYELLOW_EX,
    "info": Fore.CYAN,
    "success": Fore.LIGHTGREEN_EX,

    # Modes / timelines
    "no_leap": Fore.LIGHTBLUE_EX,
    "gregorian": Fore.LIGHTCYAN_EX,
    "astronomical": Fore.LIGHTGREEN_EX,
    "all": Fore.LIGHTYELLOW_EX,

    # Headers / emphasis
    "header": Fore.WHITE,
    "label": Fore.YELLOW,
}

# ============================================================
# Convenience Accessors
# ============================================================

def c(name: str) -> str:
    """
    Return a color by semantic name.
    Falls back to reset if the name is unknown.
    """
    return COLORS.get(name.lower(), Style.RESET_ALL)


def reset() -> str:
    """Explicit reset helper."""
    return Style.RESET_ALL