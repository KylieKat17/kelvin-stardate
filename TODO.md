# TODO – Kelvin Stardate Converter

*(Unfinished Business, Known Future Timelines, Mild Dread)*

This file tracks planned improvements, refactors, and features that are
either partially implemented, actively annoying, or clearly inevitable.

Some of these are “next steps.”
Some of these are “someday, when I have energy.”
Some of these exist because the scope got away from me.

All of them are real.

---

## 🔧 Immediate / Short-Term Fixes

Things that should probably happen sooner rather than later, because
they directly affect usability or internal consistency.

- **Unify CLI error display with `kelvin_errors.py`**
  - Error codes exist
  - Error messages exist
  - The CLI does not always display them consistently (and it's outdated),
  - ...but the errors file already does
  - This should be fixed so errors are:
    - predictable
    - clearly coded
    - styled the same way everywhere
  - This is the most immediate cleanup task

---

## 📦 Packaging & Distribution

Because at some point, running this via `python kelvin_stardate_cli.py`
will feel insufficient.

- **Make this a `pip`-installable package**
  - Installable via `pip install kelvin-stardate` (or similar)
  - CLI entry point exposed properly
  - No more “clone the repo just to run a converter”

- **Add `pyproject.toml`**
  - Modern packaging
  - Tooling sanity
  - Stop pretending `setup.py` is the future

---

## 🎨 Output, UX, & CLI Polish

Quality-of-life improvements that make the CLI nicer to live in.

- **Implement a shared `color.py` module**
  - Centralize color definitions
  - Stop redefining globals in every file
  - Make future styling changes less painful
  - Literally already exists as `colortest.py` from when I was choosing what I liked and wanted to see it againt the black Powershell background

- **Add an optional “pretty output” mode**
  - Use `tabulate` to display results in clean tables
  - Especially useful for:
    - `all` mode comparisons
    - batch conversions (future)
  - Should be optional, not default

---

## 📚 Documentation Improvements

Because this project already has too much logic to be under-documented.

- **Provide better documentation**
  - Expand README sections where useful
  - Possibly add:
    - a short usage guide
    - a design/assumptions explainer
    - examples beyond the CLI
    - pictures

---

## 📅 Calendar & Date Expansion

Features that move beyond simple conversion and into “actually useful reference tool.”

- **Add Earth day-of-week calculation**
  - Display day of the week for Earth dates
  - Unclear how annoying this will be given:
    - far-future dates
    - calendar drift assumptions
  - Worth investigating, may require explicit calendar model decisions

---

## 🧾 Canon Data & Reference Material

Because once YAML entered the chat, this became inevitable
*AKA I wrote a indexer that outputted to a yaml file and I think that*
*same functionality might be useful here*

- **Add displayable canon date information**
  - Optional mode / flag to show known canon events
  - Examples:
    - Kirk’s birthday
    - Spock’s birthday
    - Major Kelvin Timeline movie events
  - Likely stored in YAML, but format not finalized

- **Add canon reference files**
  - One file for:
    - confirmed / explicitly canon dates
  - One file for:
    - derived or inferred dates
  - These *may* end up being the same YAML file, depending on structure

---

## 🗂️ Project Metadata & History

Because projects this meticulous deserve receipts.

- **Add `CHANGELOG.md`**
  - Track notable changes
  - Possibly framed as:
    - timeline corrections
    - temporal adjustments
    - “this used to be wrong, now it isn’t”

---

## 🌀 Future / Unspecified

- Emoji support like one of my parser tools. Maybe? Probably not
- **More things I haven’t thought of yet**
  - This project keeps expanding
  - Past experience suggests this list is incomplete
  - That is fine
  - This file will be updated when the next idea hits at 1 a.m.

---

## Final Notes

This file exists so Future Me doesn’t have to reconstruct intent
from commit messages and vibes.

Not all of this needs to be done.
Some of it absolutely will be.
Some of it is aspirational.

All of it is allowed to exist here without judgment (because fuck you I didn't plan on this becoming as big as I wanted it to be)

- - -

MORE.

- make 
def prompt_mode(help_cb, error_printer):
    while True:
        raw = input(" Choose mode [default=1]: ")
        if raw.strip() == "":
            return "no_leap"
        try:
            check_user_input(raw, help_cb=help_cb)
            return normalize_mode(raw)
        except ContinuePrompt:
            continue
        except StardateCLIError as e:
            error_printer(e)
