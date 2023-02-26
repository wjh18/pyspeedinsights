import pytest

from pyspeedinsights.core.sitemap import (
    _parse_sitemap_index,
    _parse_sitemap_urls,
    _parse_urls_from_root,
    process_sitemap,
)


class TestParseSitemap:
    """Tests parsing of URLs from sitemap root."""

    def test_regular_sitemap_url_found(self, sitemap_root, sitemap_url):
        sitemap_urls = _parse_sitemap_urls(sitemap_root)
        assert sitemap_url in sitemap_urls

    def test_regular_sitemap_wrong_type_url_not_found(self, sitemap_root):
        sitemap_urls = _parse_urls_from_root(sitemap_root, type="sitemap")
        assert not sitemap_urls

    def test_sitemap_index_url_found(self, sitemap_index_root, request_url):
        sitemap_urls = _parse_sitemap_index(sitemap_index_root)
        assert request_url in sitemap_urls

    def test_sitemap_index_wrong_type_url_not_found(self, sitemap_index_root):
        sitemap_urls = _parse_urls_from_root(sitemap_index_root)
        assert not sitemap_urls


class TestProcessSitemap:
    """Tests processing of URLs from sitemap."""

    def sitemap_raises_system_exit(self, sitemap):
        with pytest.raises(SystemExit):
            process_sitemap(sitemap)

    def test_regular_sitemap_processed(self, sitemap, sitemap_url):
        num_urls = sitemap.count("<loc>")
        sitemap_urls = process_sitemap(sitemap)

        assert sitemap_url in sitemap_urls
        assert len(sitemap_urls) == num_urls

    def test_sitemap_index_processed(
        self, patch_response, sitemap_index, sitemap, sitemap_url
    ):
        num_sitemaps = sitemap_index.count("<sitemap>")
        num_urls = sitemap.count("<url>")
        patch_response(status_code=200, exception=None)
        sitemap_urls = process_sitemap(sitemap_index)

        assert sitemap_url in sitemap_urls
        assert len(sitemap_urls) == num_sitemaps * num_urls

    def test_invalid_sitemap_exits(self, sitemap_invalid):
        self.sitemap_raises_system_exit(sitemap_invalid)

    def test_invalid_sitemap_tag_exits(self, sitemap_invalid_tag):
        self.sitemap_raises_system_exit(sitemap_invalid_tag)

    def test_sitemap_no_urls_exits(self, sitemap_no_urls):
        self.sitemap_raises_system_exit(sitemap_no_urls)
