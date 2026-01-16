# test/conftest.py
# Because I hate the regular verbose terminal display
# TODO: reorder imports and shit

from collections import defaultdict
from pathlib import Path
from _pytest.terminal import TerminalReporter

import pytest # TODO: maybe remove?
import re
import shutil

from kelvin_stardate.cli.colors import c, reset

TEST_FILE_DESCRIPTIONS = {
    "test_core.py": "TESTING MAIN CONVERSION LOGIC",
    "test_validators_errors.py": "TESTING VALIDATION & ERROR CODES",
    "test_prompts_control_errors.py": "TESTING CLI CONTROL FLOW (HELP / QUIT / EMPTY)",
    "test_error_registry_complete.py": "TESTING FOR UNREGITERED ERROR CODES"
}

# ============================================================
# GLOBAL STATE
# ============================================================

_RESULTS = defaultdict(list)

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

def _visible_len(s: str) -> int:
    """Length of string ignoring ANSI escape sequences."""
    return len(_ANSI_RE.sub("", s))


# ============================================================
# CUSTOM CLI FLAG
# ============================================================

def pytest_addoption(parser):
    parser.addoption(
        "--pretty",
        action="store_true",
        default=False,
        help="Show grouped, aligned test summary by file."
    )


# ============================================================
# OUTPUT SUPPRESSION (ONLY WHEN --pretty IS USED)
# ============================================================

def pytest_configure(config):
    """
    Suppress default pytest progress output when using --pretty.
    """
    if config.getoption("--pretty"):
        config.option.verbose = 0
        config.option.quiet = 1


def pytest_report_teststatus(report, config):
    """
    Hide per-test progress symbols (dots / percentages).
    """
    if config.getoption("--pretty") and report.when == "call":
        return "", "", ""

def pytest_sessionstart(session):
    """
    Suppress pytest's per-file progress lines when using --pretty.
    """
    config = session.config
    if not config.getoption("--pretty"):
        return

    reporter = config.pluginmanager.getplugin("terminalreporter")
    if reporter:
        reporter.showfspath = False


# ============================================================
# TEST RESULT COLLECTION
# ============================================================

def _make_banner(title: str) -> str:
    """
    Create a centered banner like:
      ====== TITLE ======
    sized to the current terminal width.
    """
    width = shutil.get_terminal_size(fallback=(120, 20)).columns
    title = f" {title.strip()} "
    if width <= len(title) + 2:
        # Too narrow: just return the title
        return title.strip()

    side = (width - len(title)) // 2
    left = "=" * side
    right = "=" * (width - len(left) - len(title))
    return f"{left}{title}{right}"

def pytest_runtest_logreport(report):
    """
    Capture per-test results (call phase only).
    """
    # Defensive: some plugins can emit lists
    if isinstance(report, list):
        for r in report:
            pytest_runtest_logreport(r)
        return

    if report.when != "call":
        return

    file = report.nodeid.split("::")[0]
    test = report.nodeid.split("::")[1]

    if report.failed:
        status = "FAILED"
    elif report.skipped:
        status = "SKIPPED"
    else:
        status = "PASSED"

    _RESULTS[file].append((test, status))


def describe_test_file(path: str) -> str:
    name = Path(path).name
    return TEST_FILE_DESCRIPTIONS.get(
        name,
        "TESTING UNSPECIFIED COMPONENT"
    )


# ============================================================
# COLORSSSS
# ============================================================

def _color_status(status: str) -> str:
    if status == "PASSED":
        return f"{c('success')}{status}{reset()}"
    if status == "FAILED":
        return f"{c('error')}{status}{reset()}"
    if status == "SKIPPED":
        return f"{c('info')}{status}{reset()}"
    return status


# ============================================================
# CUSTOM KELVIN SUMMARY OUTPUT
# ============================================================

def pytest_sessionfinish(session, exitstatus):
    """
    Print custom grouped summary at the end (only with --pretty).
    """
    term_width = shutil.get_terminal_size(fallback=(120, 20)).columns

    if not session.config.getoption("--pretty"):
        return

    total = sum(len(v) for v in _RESULTS.values())
    if total == 0:
        return

    # Global alignment widths (across all files)
    all_rows = [(name, status) for tests in _RESULTS.values() for (name, status) in tests]
    name_width = max(len(name) for name, _ in all_rows)
    status_width = max(len(status) for _, status in all_rows)

    banner = _make_banner("KELVIN TEST SUMMARY")
    print(f"\n{c('info')}{banner}{reset()}\n")

    completed = 0

    # Consistent ordering by file path
    for file_path in sorted(_RESULTS.keys()):
        tests = _RESULTS[file_path]
        header = describe_test_file(file_path)
        header_line = f"{c('label')}{header}{reset()}"
        path_line = f"{c('path')}({file_path}){reset()}"
        
        print(header_line)
        print(path_line)

        for name, status in tests:
            completed += 1
            percent = int((completed / total) * 100)
            
            pct_plain = f"[{percent:>3}%]"
            pct_colored = f"{c('percent')}{pct_plain}{reset()}"

            status_colored = _color_status(status)

            # Left side (colored status, but padding computed from plain)
            left_plain = "  " + name.ljust(name_width) + "   " + status.ljust(status_width)
            left_colored = "  " + name.ljust(name_width) + "   " + status_colored.ljust(status_width + (_visible_len(status_colored) - len(status)))

            # Right-align percentage to terminal edge (use visible lengths)
            padding = term_width - _visible_len(left_colored) - _visible_len(pct_colored)
            padding = max(padding, 1)

            print(left_colored + " " * padding + pct_colored)

        print()
