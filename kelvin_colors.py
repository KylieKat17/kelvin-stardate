"""
kelvin_colors.py

Centralized color and style definitions for the Kelvin Stardate Converter.

This module exists so we do NOT have to:
- redefine color globals in every file
- remember which Fore.LIGHT_* looks readable in PowerShell
- initialize colorama more than once

If output styling changes, it should happen here.
"""

from colorama import init, Fore, Style

# Initialize colorama once, globally
init(autoreset=True)

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
# Convenience Accessors (Optional, but Nice)
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