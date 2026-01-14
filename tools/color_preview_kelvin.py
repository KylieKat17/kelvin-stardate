# color_preview_kelvin.py
# Manual visual test for CLI color rendering against black PowerShell background

from kelvin_stardate.cli.colors import COLORS, reset # type: ignore

print("\n=== Kelvin Color Palette Test ===\n")

for name, color in COLORS.items():
    print(f"{color}{name:<20}{reset()}  ← sample text for {name}")
