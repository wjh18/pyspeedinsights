import pytest


@pytest.fixture
def patch_argv(monkeypatch):
    """Fixture to patch sys.argv for testing argparse."""

    def wrapper(cmdargs, *args, **kwargs):
        monkeypatch.setattr("sys.argv", cmdargs)

    return wrapper


@pytest.fixture
def all_args():
    return [
        "psi",
        "https://www.example.com",
        "-c",
        "performance",
        "-s",
        "desktop",
        "-f",
        "json",
        "-l",
        "en",
        "-uc",
        "test-uc",
        "-us",
        "test-us",
        "-t",
        "test-ct",
    ]
