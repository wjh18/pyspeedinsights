import pytest
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

from pyspeedinsights.core.sitemap import SitemapRetrievalError, request_sitemap


class TestRequestSitemap:
    """Tests requesting sitemap text from a sitemap URL."""

    def raises_retrieval_error(self, url):
        with pytest.raises(SitemapRetrievalError):
            request_sitemap(url)

    def test_200_no_exception_returns_sitemap(
        self, patch_response, request_url, sitemap
    ):
        patch_response(status_code=200, exception=None)
        assert request_sitemap(request_url) == sitemap

    def test_200_no_exception_invalid_url_exits(self, patch_response, invalid_url):
        patch_response(status_code=200, exception=None)
        self.raises_retrieval_error(invalid_url)

    def test_404_client_error_exits(self, patch_response, request_url):
        patch_response(status_code=404, exception=HTTPError)
        self.raises_retrieval_error(request_url)

    def test_500_server_error_exits(self, patch_response, request_url):
        patch_response(status_code=500, exception=HTTPError)
        self.raises_retrieval_error(request_url)

    def test_connection_error_exits(self, patch_response, request_url):
        patch_response(status_code=None, exception=ConnectionError)
        self.raises_retrieval_error(request_url)

    def test_timeout_exits(self, patch_response, request_url):
        patch_response(status_code=None, exception=Timeout)
        self.raises_retrieval_error(request_url)

    def test_request_exception_exits(self, patch_response, request_url):
        patch_response(status_code=None, exception=RequestException)
        self.raises_retrieval_error(request_url)
