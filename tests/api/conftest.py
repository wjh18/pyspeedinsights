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
def all_metrics():
    return {
        "observedFirstPaint": 115,
        "totalCumulativeLayoutShift": 0,
        "observedFirstVisualChangeTs": 6367780394457,
        "maxPotentialFID": 16,
        "interactive": 235,
        "observedFirstMeaningfulPaint": 115,
        "cumulativeLayoutShiftMainFrame": 0,
        "observedLoadTs": 6367780371873,
        "observedLargestContentfulPaintAllFramesTs": 6367780399492,
        "observedFirstVisualChange": 110,
        "speedIndex": 235,
        "firstMeaningfulPaint": 235,
        "observedNavigationStart": 0,
        "firstContentfulPaint": 235,
        "observedSpeedIndex": 111,
        "observedNavigationStartTs": 6367780284457,
        "observedLargestContentfulPaint": 115,
        "observedTraceEndTs": 6367782718060,
        "observedCumulativeLayoutShiftMainFrame": 0,
        "observedFirstContentfulPaintTs": 6367780399492,
        "observedCumulativeLayoutShift": 0,
        "observedDomContentLoaded": 87,
        "observedTimeOrigin": 0,
        "observedLastVisualChangeTs": 6367780394457,
        "observedFirstMeaningfulPaintTs": 6367780399492,
        "totalBlockingTime": 0,
        "observedDomContentLoadedTs": 6367780371805,
        "largestContentfulPaint": 235,
        "observedLargestContentfulPaintAllFrames": 115,
        "observedLargestContentfulPaintTs": 6367780399492,
        "cumulativeLayoutShift": 0,
        "observedFirstContentfulPaint": 115,
        "observedLoad": 87,
        "observedFirstContentfulPaintAllFramesTs": 6367780399492,
        "observedLastVisualChange": 110,
        "observedSpeedIndexTs": 6367780395262,
        "observedFirstContentfulPaintAllFrames": 115,
        "observedFirstPaintTs": 6367780399492,
        "observedTraceEnd": 2434,
        "observedTimeOriginTs": 6367780284457,
    }
