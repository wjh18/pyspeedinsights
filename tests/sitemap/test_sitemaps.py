import pytest
import requests

from pyspeedinsights.core.sitemap import (
    _parse_sitemap_index,
    _parse_sitemap_urls,
    _parse_urls_from_root,
    get_sitemap_root,
    process_sitemap,
    request_sitemap,
    validate_sitemap_url,
)


class MockResponse:
    def __init__(self, text, status_code):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if 400 <= self.status_code < 600:
            raise requests.exceptions.HTTPError("Error", response=self)


@pytest.fixture
def sitemap(shared_datadir):
    return (shared_datadir / "sitemap.xml").read_text()


@pytest.fixture
def sitemap_index(shared_datadir):
    return (shared_datadir / "sitemap_index.xml").read_text()


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


class TestValidateSitemapUrl:
    def test_valid_extension_passes(self):
        assert validate_sitemap_url("example.xml")

    def test_invalid_extension_fails(self):
        assert not validate_sitemap_url("example.html")

    def test_no_extension_fails(self):
        assert not validate_sitemap_url("example")

    def test_no_filename_fails(self):
        assert not validate_sitemap_url(".xml")


def test_request_sitemap_success(monkeypatch, sitemap, request_url):
    status_code = 200

    monkeypatch.setattr(
        requests, "get", lambda *args, **kwargs: MockResponse(sitemap, status_code)
    )

    assert request_sitemap(request_url) == sitemap


def test_request_sitemap_client_error(monkeypatch, sitemap, request_url):
    status_code = 404

    monkeypatch.setattr(
        requests, "get", lambda *args, **kwargs: MockResponse(sitemap, status_code)
    )

    with pytest.raises(SystemExit):
        request_sitemap(request_url)


def test_request_sitemap_server_error(monkeypatch, sitemap, request_url):
    status_code = 500

    monkeypatch.setattr(
        requests, "get", lambda *args, **kwargs: MockResponse(sitemap, status_code)
    )

    with pytest.raises(SystemExit):
        request_sitemap(request_url)


class TestProcessSitemap:
    def test_parsing_regular_sitemap(self, sitemap_root, sitemap_url):
        sitemap_urls = _parse_sitemap_urls(sitemap_root)
        assert sitemap_url in sitemap_urls

    def test_parsing_regular_sitemap_wrong_type(self, sitemap_root):
        sitemap_urls = _parse_urls_from_root(sitemap_root, type="sitemap")
        assert not sitemap_urls

    def test_parsing_sitemap_index(self, sitemap_index_root, request_url):
        sitemap_urls = _parse_sitemap_index(sitemap_index_root)
        assert request_url in sitemap_urls

    def test_parsing_sitemap_index_wrong_type(self, sitemap_index_root):
        sitemap_urls = _parse_urls_from_root(sitemap_index_root)
        assert not sitemap_urls

    def test_processing_regular_sitemap(self, sitemap, sitemap_url):
        num_urls = sitemap.count("<loc>")

        sitemap_urls = process_sitemap(sitemap)
        assert sitemap_url in sitemap_urls
        assert len(sitemap_urls) == num_urls

    def test_processing_sitemap_index(
        self, monkeypatch, sitemap_index, sitemap, sitemap_url
    ):
        num_sitemaps = sitemap_index.count("<sitemap>")
        num_urls = sitemap.count("<url>")

        monkeypatch.setattr(
            requests, "get", lambda *args, **kwargs: MockResponse(sitemap, 200)
        )

        sitemap_urls = process_sitemap(sitemap_index)
        assert sitemap_url in sitemap_urls
        assert len(sitemap_urls) == num_sitemaps * num_urls
