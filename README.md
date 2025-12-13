# Kelvin Stardate Converter  
*(CLI + Library, Multiple Timelines, Mild Exhaustion)*

This is a **Kelvin Timeline–compatible stardate ⟷ Earth date converter**, written in Python, with both:

- a **fully interactive terminal interface**, and  
- a **scriptable CLI / importable library**  

It exists because:
1. Stardates are fake,
2. Some people pretend they aren’t,
3. I got tired of hand-waving calendar math across timelines, and
4. Nobody else open-sourced one that does the canonical conversion for the reboot movies.

Also because I kept needing it.

This project is *far more complicated than it strictly needed to be*, and that is on purpose.

---

## What This Actually Does

You can convert:

- **Earth dates → Stardates**
- **Stardates → Earth dates**

Using **multiple competing calendar models**, because timekeeping is political and Star Trek made it worse.

### Supported Models / “Modes”

| Mode | Description |
|-----|------------|
| `no_leap` | **Orci-style ordinal year** (365 days, no leap years). Clean. Canon-adjacent. Emotionally stable. |
| `gregorian` | Real Earth leap-year rules. Messy, but honest. |
| `astronomical` | Fractional year model (365.2425 days). For people who enjoy decimals and consequences. |
| `all` | Shows **every result side-by-side**, because sometimes you just want to see the damage. |

The CLI color-codes output by mode so you can tell which timeline you’re in without reading too closely.

---

## Requirements

- **Python 3.9+**
- `pip` (installed and not ancient)

Install dependencies with:

```bash
pip install -r requirements.txt
````

New to Python or the command line? See [`SETUP_FOR_DUMMIES.md`](./SETUP_FOR_DUMMIES.md)

### Python Dependencies

Dependencies are intentionally minimal and explicit:

| Package    | Purpose                                                                      |
| ---------- | ---------------------------------------------------------------------------- |
| `colorama` | Cross-platform terminal colors (especially required on Windows / PowerShell) |
| `pytest`   | Required to run `test_kelvin_stardate.py`                                    |
| `PyYAML`   | Planned future functionality (configuration / structured data support)       |

Only `colorama` is required to *run the CLI*.
`pytest` is only needed if you are running tests.

---

## Environment & System Information

This project was developed and tested in a very specific environment.
Other setups *should* work, but this is what I was working with:

### Tested Environment

- **Operating System:** Microsoft Windows 11 Pro
  Version 10.0.26100 (Build 26100)
- **Python:** CPython 3.13.9
- **pip:** 25.2
- **Architecture:** 64-bit (AMD64)
- **Terminal:** PowerShell / Windows Terminal (dark mode)
- **Locale:** en_US (cp1252)
- **stdout encoding:** UTF-8

CLI output (colors, spacing, box characters) was tuned for PowerShell and Windows Terminal.
If your terminal ignores ANSI colors, output will still work, but will be less readable.

### Python Version Notes

- Developed and tested on **Python 3.13.9** (originally 3.9+ when I was still on the Windows store download)
- Uses only standard library features and widely supported packages
- Python ≥ 3.9 is required
- Not tested on PyPy
- Not tested on Python < 3.9

If this fails on older Python versions, that is not a bug — upgrade Python.

### pip Notes

You should have `pip` installed and reasonably up to date.

Recommended sanity check:

```bash
python -m pip install --upgrade pip
```

If `pip` is missing, install Python properly from
[https://www.python.org/downloads/](https://www.python.org/downloads/)

Do not attempt to duct-tape this with system Python from 2014.

---

## Running the CLI

You have three ways to use this, depending on how awake you are.

---

### 1. Interactive Mode (Default)

Just run:

```bash
python kelvin_stardate_cli.py
```

You’ll get a menu-driven interface with:

- mode selection
- month name parsing (yes, you can type “September”)
- leap-year validation
- error codes
- polite exits
- and a banner that quietly implies too much lore knowledge

This is the “I just want an answer” mode.

---

### 2. Subcommands (Script-Friendly)

Earth → Stardate:

```bash
python kelvin_stardate_cli.py earth-to 2258 4 17 --mode gregorian
```

Stardate → Earth:

```bash
python kelvin_stardate_cli.py sd-to 2258.42 --mode astronomical
```

If you don’t specify a mode, it defaults to `no_leap`.
*(And all mode flags do have pseudonyms. Because I'd rather type `a` or `astro` rather than `astronomical`, wouldn't you? Use -h for more info)*

---

### 3. Flags (Minimal Typing)

Earth date → Stardate:

```bash
python kelvin_stardate_cli.py --from-earth 2258-04-17 --mode all
```

Stardate → Earth date:

```bash
python kelvin_stardate_cli.py --from-sd 2258.42
```

If you give it *nothing*, it drops you back into interactive mode instead of yelling at you.

---

## Output Behavior (On Purpose)

- Inputs are always echoed at the top of results
- Outputs include both **ISO dates** and **human-readable dates**
- `all` mode prints a comparison block so you can see exactly how bad the divergence is
- Errors use **coded messages** (`E001`, `E002`, etc.) because vague failure is worse than explicit failure

The CLI also attempts to auto-detect whether a stardate looks:

- Kelvin-style, or
- Astronomical (long fractional component)

This is not magic. It is pattern recognition and vibes.

---

## Library Usage (If You’re Importing This)

You can also just use the math.

```python
from kelvin_stardate import earth_to_stardate, stardate_to_earth
from datetime import date

sd = earth_to_stardate(date(2258, 4, 17), mode="no_leap")
dt = stardate_to_earth("2258.42", mode="gregorian")
```

Astronomical versions are explicit:

```python
from kelvin_stardate import (
    earth_to_stardate_astronomical,
    stardate_to_earth_astronomical
)
```

They use a continuous-year model and do not pretend leap days are clean.

---

## Running Tests

Tests are written using `pytest`

To run the full test suite:

```bash
pytest
```

Running tests requires `pytest` to be installed
(see `requirements.txt`).

---

## Project Structure (at present)

```text
.
├── kelvin_stardate.py            # Core conversion logic (the math nobody agrees on)
├── kelvin_stardate_cli.py        # CLI, interactive menu, argument parsing, output
├── kelvin_errors.py              # Custom exception + error codes
├── kelvin_help.py                # Help text & redisplay loop
├── tests/                        # Test stuff, duh. Don't wanna do that shit by hand
│   └── test_kelvin_stardate.py
├── references/
│   ├── canon_dates.yaml          # might be implemented in future
│   ├── scripts/                  # movie scripts I used for reference when checking dates
│   ├── source_notes.md           # might be added later
│   └── LICENSE
├── requirements.txt            # Runtime + test dependencies
├── .gitignore                  # Aggressively preventative
├── README.md                   # You are here
└── LICENSE
```

---

## Design Notes / Why This Is Like This

- Stardates are **not canonically defined**, so pretending there’s One True Formula is dishonest.
- This tool makes the assumptions explicit and lets you choose.
- The Kelvin Timeline uses **ordinal thinking**, not Earth calendar purity.
- Astronomical mode exists because sometimes you want math, not vibes.
- `all` mode exists because sometimes you want to *see the timeline fracture*.

Also:
Yes, this CLI is more defensive than strictly necessary.
No, I don’t regret that.

---

## Roadmap

This project is stable and usable as-is, but there are several planned improvements
and expansions, ranging from quality-of-life fixes to larger structural changes.

Short version:

- CLI polish and internal cleanup
- Proper packaging and distribution
- Better output options and documentation
- Canon-reference data support

Long version lives in [`TODO.md`](./TODO.md), which tracks:
- immediate fixes
- packaging plans
- UX improvements
- canon data handling
- and whatever else Future Me decides is necessary

Nothing here is time-bound.
Some of it will happen soon.
Some of it will happen when I feel like it.
That is intentional.

---

## Known Limitations

- This does **not** attempt to reconcile Prime Timeline stardates (sorry, there are already tools for that. Go check one of them!)
- This does **not** handle BCE dates (...why would you want that anyway? I don't see Jesus walking around on camera, do you?)
- This will not stop you from creating paradoxes.
- The universe will not thank you.

---

## Licensing & Usage Notes

This repository contains **both original code and reference material**, which are licensed differently.

- **Code** (all `.py` files, CLI, tests) is licensed under  
  **Creative Commons Attribution–NonCommercial 4.0 (CC BY-NC 4.0)**  
  → Non-commercial use only; attribution required.

- **Reference material** (everything under `/references`) is licensed under  
  **Creative Commons Attribution–NonCommercial–ShareAlike 4.0 (CC BY-NC-SA 4.0)**  
  → Non-commercial use only; attribution required; derivatives must use the same license.  
  → Reference data may not be redistributed independently of this project.

This project is not affiliated with, endorsed by, or claiming authority over
official Star Trek canon.


---

## Final Note

This started as “I just need a quick converter” and became
“well, *now* it needs modes, error codes, command line flags, and an interactive menu.”

If you’re reading this because you found the repo:
hello, welcome, I hope this saves you time.

If you’re reading this because you’re me, later:
yes, this was the correct amount of effort.
