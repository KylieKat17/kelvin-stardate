# Kelvin Stardate Converter  
*(CLI + Library, Multiple Timelines, Mild Exhaustion)*

This is a **Kelvin Timeline–compatible stardate ⟷ Earth date converter**, written in Python, with both:

- a **fully interactive terminal interface**, and  
- a **scriptable CLI / importable library**  

It exists because:
1. Stardates are fake,
2. Everyone pretends they aren’t, and
3. I got tired of hand-waving calendar math across timelines.
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
- One (1) external dependency:

```bash
pip install -r requirements.txt
````

Which installs:

* `colorama` – for readable output that doesn’t look like a warp core breach in PowerShell

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

* mode selection
* month name parsing (yes, you can type “September”)
* leap-year validation
* error codes
* polite exits
* and a banner that quietly implies too much lore knowledge

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


## Output Behavior (On Purpose)

* Inputs are always echoed at the top of results
* Outputs include both **ISO dates** and **human-readable dates**
* `all` mode prints a comparison block so you can see exactly how bad the divergence is
* Errors use **coded messages** (`E001`, `E002`, etc.) because vague failure is worse than explicit failure

The CLI also attempts to auto-detect whether a stardate looks:

* Kelvin-style, or
* Astronomical (long fractional component)

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

## Project Structure

```text
.
├── kelvin_stardate.py          # Core conversion logic (the math nobody agrees on)
├── kelvin_stardate_cli.py      # CLI, interactive menu, argument parsing, output
├── kelvin_errors.py            # Custom exception + error codes
├── kelvin_help.py              # Help text & redisplay loop
├── requirements.txt            # Minimal dependencies
├── .gitignore                  # Aggressively preventative
└── README.md                   # You are here
```

---

## Design Notes / Why This Is Like This

* Stardates are **not canonically defined**, so pretending there’s One True Formula is dishonest.
* This tool makes the assumptions explicit and lets you choose.
* The Kelvin Timeline uses **ordinal thinking**, not Earth calendar purity.
* Astronomical mode exists because sometimes you want math, not vibes.
* `all` mode exists because sometimes you want to *see the timeline fracture*.

Also:
Yes, this CLI is more defensive than strictly necessary.
No, I don’t regret that.

---

## Known Limitations

* This does **not** attempt to reconcile Prime Timeline stardates.
* This does **not** handle BCE dates.
* This will not stop you from creating paradoxes.
* The universe will not thank you.

---

## License

MIT License.
Use it, fork it, improve it, or ignore it until you rediscover it at 2 a.m.

---

## Final Note

This started as “I just need a quick converter” and became
“well, *now* it needs modes, error codes, and an interactive menu.”

If you’re reading this because you found the repo:
hello, welcome, I hope this saves you time.

If you’re reading this because you’re me, later:
yes, this was the correct amount of effort
