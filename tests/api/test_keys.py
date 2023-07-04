import keyring
import pytest
from keyring.errors import KeyringError

from pyspeedinsights.api.keys import get_api_key


class TestKeyRetrieval:
    def throw_keyringerror(self):
        raise KeyringError

    def throws_keyringerror(self):
        with pytest.raises(KeyringError):
            get_api_key()

    def test_key_found(self, patch_keyring):
        mock_pw = "secret"
        patch_keyring(mock_pw)
        assert get_api_key() == mock_pw

    def test_key_not_found_exception(self, monkeypatch, patch_input, capsys):
        monkeypatch.setattr(
            keyring, "get_password", lambda *args, **kwargs: self.throw_keyringerror()
        )
        patch_input(mock_input="secret")  # Placeholder to avoid stdin errors

        get_api_key()
        out = capsys.readouterr().out  # Printed when KeyringError is caught
        assert "There was an error retrieving your API key from the keystore: " in out

    def test_key_not_found_fallback_success(self, patch_keyring, patch_input):
        patch_keyring(mock_pw=None)
        mock_input = "secret"
        patch_input(mock_input)
        assert get_api_key() == mock_input

    def test_key_not_found_fallback_retry_success(
        self, patch_iter_input, patch_keyring
    ):
        patch_keyring(mock_pw=None)
        successful_input = "secret"
        inputs = iter(["", successful_input])  # Retry then successful input
        patch_iter_input(inputs)
        assert get_api_key() == successful_input

    def test_key_not_found_fallback_retry_quit(self, patch_iter_input, patch_keyring):
        patch_keyring(mock_pw=None)
        inputs = iter(["", "Q"])  # Retry then quit
        patch_iter_input(inputs)
        self.throws_keyringerror()

    def test_key_not_found_fallback_retry_limit_hit(self, patch_input, patch_keyring):
        patch_keyring(mock_pw=None)
        patch_input(mock_input="")  # Empty input will eventually hit limit
        self.throws_keyringerror()
