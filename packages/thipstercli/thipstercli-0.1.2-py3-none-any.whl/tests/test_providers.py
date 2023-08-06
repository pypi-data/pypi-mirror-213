from typer.testing import CliRunner
from thipstercli.state import state
from thipstercli.providers import app, get_provider_class, check_provider_exists

runner = CliRunner(mix_stderr=False)

providers = [
    "google",
]


def test_list_providers():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    for provider in providers:
        assert provider in result.stdout.lower()


def test_info_provider():
    result = runner.invoke(app, ["info", "google"])
    assert result.exit_code == 0
    assert "google" in result.stdout.lower()
    assert "gcloud" in result.stdout.lower()


def test_set_provider():
    result = runner.invoke(app, ["set", "google"])
    assert result.exit_code == 0
    assert "google" in result.stdout.lower()
    assert "provider set to" in result.stdout.lower()

    result = runner.invoke(app, ["display"])
    assert result.exit_code == 0
    assert "google" in result.stdout.lower()
    assert "provider set to" in result.stdout.lower()


def test_get_provider_class():
    provider = get_provider_class("Google")
    assert provider.__name__ == "GoogleAuth"


def test_check_provider_exists():
    state["providers"] = ["Google.py"]
    provider = check_provider_exists("google")
    assert provider == "Google"
