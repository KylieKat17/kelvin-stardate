import yaml
from pathlib import Path
from datetime import date
from colorama import Fore, Style, init

init(autoreset=True)

CANON_PATH = Path("data/canon_confirmed.yaml")


class CanonDumper(yaml.SafeDumper):
    pass


def _increase_indent(self, flow=False, indentless=False):
    return super(CanonDumper, self)._increase_indent(flow, False)


CanonDumper.increase_indent = _increase_indent

# -----------------------------
# Utilities
# -----------------------------

def load_canon():
    if CANON_PATH.exists():
        with open(CANON_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}

def save_canon(data):
    CANON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CANON_PATH, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def prompt(text, allow_blank=False):
    try:
        val = input(text).strip()
    except EOFError:
        val = "q"

    if val.lower() == "q":
        print(f"\n{Fore.YELLOW}Quit requested — saving progress.{Style.RESET_ALL}")
        raise SystemExit

    if not val and not allow_blank:
        return prompt(text, allow_blank)

    return val

def iso_date_prompt(label):
    while True:
        raw = prompt(f"{label} (YYYY-MM-DD): ")
        try:
            date.fromisoformat(raw)
            return raw
        except ValueError:
            print(f"{Fore.RED}Invalid ISO date. Try again.{Style.RESET_ALL}")

# -----------------------------
# Entry Creators
# -----------------------------

def add_character(data):
    chars = data.setdefault("characters", {})

    cid = prompt("Character ID (snake_case): ")
    if cid in chars:
        print(f"{Fore.RED}Character '{cid}' already exists.{Style.RESET_ALL}")
        return

    name = prompt("Display name: ")
    species = prompt("Species: ", allow_blank=True)

    nick_raw = prompt("Nicknames (comma-separated, optional): ", allow_blank=True)
    nicknames = [n.strip() for n in nick_raw.split(",") if n.strip()]

    earth_date = iso_date_prompt("Birth Earth date")
    stardate = prompt("Birth stardate (Kelvin, optional): ", allow_blank=True)

    source = prompt("Source: ")
    source_type = prompt("Source type (film, film_supplement, novelization, etc.): ", allow_blank=True)
    confidence = prompt("Confidence (canon/approximate/disputed): ")

    entry = {
        "id": cid,
        "name": name,
        "species": species or None,
        "birth": {
            "earth_date": earth_date,
            "confidence": confidence,
            "source": source,
        }
    }

    if nicknames:
        entry["nicknames"] = nicknames

    if stardate:
        entry["birth"]["stardate_kelvin"] = float(stardate)

    if source_type:
        entry["birth"]["source_type"] = source_type

    chars[cid] = entry
    print(f"{Fore.GREEN}Added character '{cid}'.{Style.RESET_ALL}")

def add_event(data):
    events = data.setdefault("events", {})

    eid = prompt("Event ID (snake_case): ")
    if eid in events:
        print(f"{Fore.RED}Event '{eid}' already exists.{Style.RESET_ALL}")
        return

    desc = prompt("Description: ")
    earth_date = iso_date_prompt("Event Earth date")
    source = prompt("Source: ")
    confidence = prompt("Confidence (canon/approximate/disputed): ")

    events[eid] = {
        "id": eid,
        "description": desc,
        "earth_date": earth_date,
        "confidence": confidence,
        "source": source,
    }

    print(f"{Fore.GREEN}Added event '{eid}'.{Style.RESET_ALL}")

# -----------------------------
# Menu
# -----------------------------

def main():
    data = load_canon()

    print(f"{Fore.CYAN}Canon Data Editor — Kelvin Timeline{Style.RESET_ALL}")
    print("Type 'q' at any prompt to quit.\n")

    while True:
        print("Choose an action:")
        print("  1) Add character")
        print("  2) Add event")
        print("  q) Quit")
        choice = prompt("> ", allow_blank=True)

        try:
            if choice == "1":
                add_character(data)
            elif choice == "2":
                add_event(data)
            elif choice.lower() == "q":
                raise SystemExit
            else:
                print("Invalid choice.")
                continue

            save_canon(data)
            print(f"{Fore.CYAN}Saved → {CANON_PATH}{Style.RESET_ALL}\n")

        except SystemExit:
            save_canon(data)
            print(f"{Fore.GREEN}Final save complete. Exiting.{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    main()
