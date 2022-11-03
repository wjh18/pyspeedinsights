import pytest
import requests
from requests.exceptions import HTTPError, RequestException

from pyspeedinsights.core.sitemap import get_sitemap_root


class MockResponse:
    """Mock response used to patch requests.Response objects"""

    def __init__(self, text: str, status_code: int, exception: RequestException = None):
        self.text = text  # requests.Response.text
        self.status_code = status_code  # requests.Response.status_code
        self.exception = exception  # Custom exception
        if self.exception:
            self.raise_for_exception()

    def raise_for_status(self):
        if 400 <= self.status_code < 600 and self.exception:
            raise HTTPError("Error", response=self)

    def raise_for_exception(self):
        """Response.raise_for_status() only throws HTTPError"""
        raise self.exception("Error")


@pytest.fixture
def patch_response(monkeypatch, sitemap):
    """Fixture to patch response with custom status_code and exception"""

    def wrapper(status_code=200, exception=None, *args, **kwargs):
        monkeypatch.setattr(
            requests,
            "get",
            lambda *args, **kwargs: MockResponse(sitemap, status_code, exception),
        )

    return wrapper


@pytest.fixture
def sitemap(shared_datadir):
    # shared_datadir is a fixture provided by pytest-datadir
    return (shared_datadir / "sitemap.xml").read_text()


@pytest.fixture
def sitemap_index(shared_datadir):
    return (shared_datadir / "sitemap_index.xml").read_text()


@pytest.fixture
def sitemap_invalid(shared_datadir):
    return (shared_datadir / "sitemap_invalid.xml").read_text()


@pytest.fixture
def sitemap_invalid_tag(shared_datadir):
    return (shared_datadir / "sitemap_invalid_tag.xml").read_text()


@pytest.fixture
def sitemap_no_urls(shared_datadir):
    return (shared_datadir / "sitemap_no_urls.xml").read_text()


@pytest.fixture
def sitemap_root(sitemap):
    return get_sitemap_root(sitemap)


@pytest.fixture
def sitemap_index_root(sitemap_index):
    return get_sitemap_root(sitemap_index)


@pytest.fixture
def request_url():
    return "https://www.example.com/sitemap.xml"


@pytest.fixture
def sitemap_url():
    return "https://www.example.com/"


@pytest.fixture
def invalid_url():
    return "https://www.example.com/sitemap.html"
