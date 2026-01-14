# Kelvin Stardate Converter  

*(CLI + Library, Multiple Timelines, Mild Exhaustion)*

This is a **Kelvin Timeline–compatible stardate ⟷ Earth date converter**, written in Python, providing both:

- a **fully interactive command-line interface**, and  
- a **clean, importable Python library**  

It exists because:

1. Stardates are fake,  
2. Some people pretend they aren’t,  
3. Star Trek (2009–2016) made calendar math everyone’s problem, and  
4. Nobody else open-sourced a converter that actually matches the reboot-era assumptions.

Also because I kept needing it.

This project is **more complicated than strictly necessary**, and that is intentional.

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
- `pip`
- A terminal (PowerShell or Command Prompt on Windows)

If you just want it to work and do not enjoy tooling:
👉 see [`SETUP_FOR_DUMMIES.md`](./SETUP_FOR_DUMMIES.md)

---

## Installation (Recommended)

This project uses modern Python packaging (`pyproject.toml`) and should be installed inside a **virtual environment**.

From the project root, with a venv activated:

```bash
pip install -e .
```

This:

* installs runtime dependencies
* registers the `kelvin-stardate` command
* keeps the source editable

---

## Running the CLI

Once installed, run:

```bash
kelvin-stardate
```

This launches the **interactive menu**, which supports:

* mode selection
* month name parsing (yes, “September” works)
* leap-year validation
* explicit error codes
* polite exits
* a banner that implies too much timeline awareness

This is the **default and recommended** way to use the tool.

---

## CLI Behavior (On Purpose)

* Inputs are echoed before results
* Output includes both **ISO dates** and **human-readable dates**
* `all` mode prints a comparison block so you can see divergence clearly
* Errors use **coded messages** (`E001`, `E002`, etc.) because vague failure is worse than explicit failure

The CLI also attempts to auto-detect whether a stardate looks:

* Kelvin-style (ordinal), or
* Astronomical (long fractional component)

This is not magic. It is pattern recognition and vibes.

---

## Library Usage (If You’re Importing This)

You can also use the conversion logic directly:

```python
from datetime import date
from kelvin_stardate.core import earth_to_stardate, stardate_to_earth

sd = earth_to_stardate(date(2258, 4, 17), leap_mode="no_leap")
dt = stardate_to_earth("2258.42", leap_mode="gregorian")
```

Astronomical conversions are explicit:

```python
from kelvin_stardate import (
    earth_to_stardate_astronomical,
    stardate_to_earth_astronomical,
)
```

They use a continuous-year model and do not pretend leap days are tidy.

---

## Running Tests

Tests use **pytest**.

From the project root (inside the venv):

```bash
pytest
```

---

## Project Structure (Current & Public)

```text
.
├── src/
│   └── kelvin_stardate/
│       ├── core.py              # Conversion logic
│       ├── validators.py        # Input validation rules
│       ├── errors.py            # Error codes + exceptions
│       ├── data/
│       │   └── canon_confirmed.yaml
│       └── cli/
│           ├── main.py          # CLI entrypoint
│           ├── prompts.py       # Input loops
│           ├── helptext.py      # Help output
│           └── colors.py        # Terminal formatting
│
├── tools/                       # Developer utilities (not unit tests)
├── tests/                       # pytest test suite
├── SETUP_FOR_DUMMIES.md
├── README.md
├── pyproject.toml
├── requirements.txt             # Convenience only
└── LICENSE
```

---

## Design Notes / Why This Is Like This

* Kelvin Stardates are **not canonically defined**, so pretending there’s One True Formula is dishonest.
* This tool makes assumptions explicit and lets you choose.
* The Kelvin Timeline uses **ordinal thinking**, not Earth calendar purity.
* Astronomical mode exists because sometimes you want math, not vibes.
* `all` mode exists because sometimes you want to *see the timeline fracture*.

Yes, the CLI is more defensive than strictly necessary.
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

* This does **not** attempt to reconcile Prime Timeline stardates (sorry, there are already tools for that. Go check one of them!)
* This does **not** handle BCE dates (...why would you want that anyway? I don't see Jesus walking around on camera, do you?)
* This will not stop you from creating paradoxes.
* The universe will not thank you.

---

## Licensing & Usage Notes

This repository contains **both original code and reference material**, licensed separately:

* **Code** (all `.py` files, CLI, tests):
  **Creative Commons Attribution–NonCommercial 4.0 (CC BY-NC 4.0)**

* **Reference material** (`/references`):
  **Creative Commons Attribution–NonCommercial–ShareAlike 4.0 (CC BY-NC-SA 4.0)**

This project is not affiliated with, endorsed by, or claiming authority over
official Star Trek canon.

---

## Final Note

This started as “I just need a quick converter” and became
“well, *now* it needs modes, error codes, packaging, and a real CLI.”

If you found this repo:
welcome — I hope it saves you time.

If you are Future Me:
yes, this was the correct amount of effort.