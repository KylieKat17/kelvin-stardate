from kelvin_stardate.cli.colors import COLORS, reset

print("\n=== Kelvin Color Palette Test ===\n")

for name, color in COLORS.items():
    print(f"{color}{name:<20}{reset()}  ← sample text for {name}")
