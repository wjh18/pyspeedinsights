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


@pytest.fixture
def metrics_json():
    return {
        "CUMULATIVE_LAYOUT_SHIFT_SCORE": {"distributions": [{"proportion": 0.99}]},
        "EXPERIMENTAL_INTERACTION_TO_NEXT_PAINT": {
            "distributions": [{"proportion": 0.94}]
        },
        "EXPERIMENTAL_TIME_TO_FIRST_BYTE": {"distributions": [{"proportion": 0.93}]},
        "FIRST_CONTENTFUL_PAINT_MS": {"distributions": [{"proportion": 0.98}]},
        "FIRST_INPUT_DELAY_MS": {"distributions": [{"proportion": 0.96}]},
        "INTERACTION_TO_NEXT_PAINT": {"distributions": [{"proportion": 0.95}]},
        "LARGEST_CONTENTFUL_PAINT_MS": {"distributions": [{"proportion": 0.97}]},
    }
