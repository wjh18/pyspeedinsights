import keyring
import pytest
from keyring.errors import KeyringError

from pyspeedinsights.api.keys import get_api_key


def test_key_found(monkeypatch):
    mock_pw = "secret"
    monkeypatch.setattr(keyring, "get_password", lambda *args, **kwargs: mock_pw)
    assert get_api_key() == mock_pw


def test_key_not_found_fallback(monkeypatch):
    mock_pw = None
    monkeypatch.setattr(keyring, "get_password", lambda *args, **kwargs: mock_pw)
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "secret")
    assert get_api_key() == "secret"


def test_key_not_found_fallback_exception(monkeypatch, capsys):
    def throw_keyring_exception():
        raise KeyringError

    monkeypatch.setattr(
        keyring, "get_password", lambda *args, **kwargs: throw_keyring_exception()
    )
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "secret")

    get_api_key()
    out = capsys.readouterr().out
    assert out == "There was an error retrieving your API key from the keystore.\n"


def test_key_not_found_fallback_retry_success(monkeypatch):
    mock_pw = None
    monkeypatch.setattr(keyring, "get_password", lambda *args, **kwargs: mock_pw)
    inputs = iter(["", "secret"])  # Retry then successful input
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))
    assert get_api_key() == "secret"


def test_key_not_found_fallback_retry_quit(monkeypatch):
    mock_pw = None
    monkeypatch.setattr(keyring, "get_password", lambda *args, **kwargs: mock_pw)
    inputs = iter(["", "Q"])  # Retry then quit
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))
    with pytest.raises(SystemExit):
        get_api_key()


def test_key_not_found_fallback_retry_limit_hit(monkeypatch):
    mock_pw = None
    monkeypatch.setattr(keyring, "get_password", lambda *args, **kwargs: mock_pw)
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")
    with pytest.raises(SystemExit):
        get_api_key()
