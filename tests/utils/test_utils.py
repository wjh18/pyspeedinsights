import pytest

from pyspeedinsights.utils.generic import (
    remove_dupes_from_list,
    remove_nonetype_dict_items,
    sort_dict_alpha,
)
from pyspeedinsights.utils.urls import validate_url


class TestValidateUrl:
    """Tests validation of URLs."""

    def raises_system_exit(self, url):
        with pytest.raises(SystemExit):
            validate_url(url)

    def test_url_without_tld_exits(self):
        self.raises_system_exit("badurl")

    def test_url_without_tld_with_path_exits(self):
        self.raises_system_exit("badurl/path")

    def test_url_with_path_and_extension_without_tld_exits(self):
        self.raises_system_exit("badurl/path.html")

    def test_valid_urls_are_not_modified(self):
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
        url = "example.com"
        mod_url = validate_url(url)
        assert mod_url == "https://" + url

    def test_missing_scheme_is_added_with_path(self):
        url = "example.com/hello"
        mod_url = validate_url(url)
        assert mod_url == "https://" + url

    def test_missing_scheme_is_added_with_filepath(self):
        url = "example.com/hello.xml"
        mod_url = validate_url(url)
        assert mod_url == "https://" + url

    def test_missing_scheme_is_added_with_subdomain(self):
        url = "www.example.com"
        mod_url = validate_url(url)
        assert mod_url == "https://" + url

    def test_missing_scheme_is_added_with_subdomain_and_path(self):
        url = "www.example.com/hello"
        mod_url = validate_url(url)
        assert mod_url == "https://" + url

    def test_missing_scheme_is_added_with_subdomain_and_filepath(self):
        url = "www.example.com/hello.xml"
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


class TestDictUtils:
    """Tests dictionary utilities."""

    dct = {1: None, 2: None, 3: "test"}
    dct2 = {"test": 1, "zest": 2, "lest": 3, "rest": 4}

    def test_none_is_removed(self):
        mod_dct = remove_nonetype_dict_items(self.dct)
        assert None not in mod_dct.values()

    def test_sort_dict_alphabetically(self):
        s_dct = sort_dict_alpha(self.dct2)
        assert list(s_dct.keys()) == ["lest", "rest", "test", "zest"]


class TestDedupeList:
    """Tests remove_dupes_from_list() utility."""

    s, d, md = 1, 2, 3
    lst = [s] * s + [d] * d + [md] * md

    def test_single_occurences_are_not_removed(self):
        assert remove_dupes_from_list(self.lst).count(self.s) == self.s

    def test_duplicates_are_removed(self):
        assert remove_dupes_from_list(self.lst).count(self.d) == self.s

    def test_multiple_duplicates_are_removed(self):
        assert remove_dupes_from_list(self.lst).count(self.md) == self.s
