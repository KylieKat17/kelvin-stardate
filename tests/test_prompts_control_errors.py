import pytest

from kelvin_stardate.errors import StardateCLIError
from kelvin_stardate.cli.prompts import ContinuePrompt, check_user_input


def test_check_user_input_empty_raises_E001():
    with pytest.raises(StardateCLIError) as excinfo:
        check_user_input("")
    assert excinfo.value.code == "E001"


def test_check_user_input_help_raises_ContinuePrompt_and_calls_help_cb():
    called = {"ok": False}

    def help_cb():
        called["ok"] = True

    with pytest.raises(ContinuePrompt):
        check_user_input("h", help_cb=help_cb)

    assert called["ok"] is True


def test_check_user_input_quit_raises_SystemExit():
    with pytest.raises(SystemExit):
        check_user_input("q")
