import pytest

from pyspeedinsights.utils.generic import (
    remove_dupes_from_list,
    remove_nonetype_dict_items,
    sort_dict_alpha,
)
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


class TestDictUtils:
    dct = {1: None, 2: None, 3: "test"}
    dct2 = {"test": 1, "zest": 2, "lest": 3, "rest": 4}

    def test_none_is_removed(self):
        mod_dct = remove_nonetype_dict_items(self.dct)
        assert None not in mod_dct.values()

    def test_sort_dict_alphabetically(self):
        s_dct = sort_dict_alpha(self.dct2)
        assert list(s_dct.keys()) == ["lest", "rest", "test", "zest"]


class TestDedupeList:
    s = 1
    d = 2
    md = 3
    lst = [s] * s + [d] * d + [md] * md

    def test_single_occurences_are_not_removed(self):
        assert remove_dupes_from_list(self.lst).count(self.s) == self.s

    def test_duplicates_are_removed(self):
        assert remove_dupes_from_list(self.lst).count(self.d) == self.s

    def test_multiple_duplicates_are_removed(self):
        assert remove_dupes_from_list(self.lst).count(self.md) == self.s
