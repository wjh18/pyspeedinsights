import keyring
import pytest


@pytest.fixture
def patch_keyring(monkeypatch):
    def wrapper(mock_pw, *args, **kwargs):
        monkeypatch.setattr(keyring, "get_password", lambda *args, **kwargs: mock_pw)

    return wrapper


@pytest.fixture
def patch_input(monkeypatch):
    def wrapper(mock_input, *args, **kwargs):
        monkeypatch.setattr("builtins.input", lambda *args, **kwargs: mock_input)

    return wrapper


@pytest.fixture
def patch_iter_input(monkeypatch):
    """Supports multiple input patching via iterable"""

    def wrapper(inputs, *args, **kwargs):
        monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))

    return wrapper
