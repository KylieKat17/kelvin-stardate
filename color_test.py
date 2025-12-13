from colorama import init, Fore, Style
init()

colors = {
    "BLACK": Fore.BLACK,
    "RED": Fore.RED,
    "GREEN": Fore.GREEN,
    "YELLOW": Fore.YELLOW,
    "BLUE": Fore.BLUE,
    "MAGENTA": Fore.MAGENTA,
    "CYAN": Fore.CYAN,
    "WHITE": Fore.WHITE,
    "LIGHTBLACK_EX": Fore.LIGHTBLACK_EX,
    "LIGHTRED_EX": Fore.LIGHTRED_EX,
    "LIGHTGREEN_EX": Fore.LIGHTGREEN_EX,
    "LIGHTYELLOW_EX": Fore.LIGHTYELLOW_EX,
    "LIGHTBLUE_EX": Fore.LIGHTBLUE_EX,
    "LIGHTMAGENTA_EX": Fore.LIGHTMAGENTA_EX,
    "LIGHTCYAN_EX": Fore.LIGHTCYAN_EX,
    "LIGHTWHITE_EX": Fore.LIGHTWHITE_EX,
}

print("\n=== Colorama Foreground Color Test ===\n")

for name, color in colors.items():
    print(f"{color}{name:<20}{Style.RESET_ALL}  ← sample text in {name}")

