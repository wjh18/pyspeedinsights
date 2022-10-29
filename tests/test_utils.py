import pytest

from pyspeedinsights.utils.urls import validate_url


class TestValidateUrl:
    def test_exit_for_url_without_tld(self):
        with pytest.raises(SystemExit):
            validate_url("badurl")

    def test_exit_for_url_without_tld_with_path(self):
        with pytest.raises(SystemExit):
            validate_url("badurl/path")

    def test_exit_for_url_without_tld_with_path_and_extension(self):
        with pytest.raises(SystemExit):
            validate_url("badurl/path.html")

    def test_valid_urls_not_modified(self):
        urls = [
            "https://www.example.com",
            "https://example.com",
            "https://www.example.com/path",
            "https://www.example.com/path.html",
        ]
        for url in urls:
            mod_url = validate_url(url)
            assert mod_url == url

    def test_missing_scheme_is_added(self):
        url = "www.example.com"
        mod_url = validate_url(url)
        assert mod_url == "https://" + url

    def test_url_fragment_is_removed(self):
        url = "https://example.com/hello#test"
        mod_url = validate_url(url)
        assert mod_url == url.split("#")[0]

    def test_query_params_are_removed(self):
        url = "https://example.com/hello?test=test&test2=test2"
        mod_url = validate_url(url)
        assert mod_url == url.split("?")[0]
