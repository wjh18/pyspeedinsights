from pyspeedinsights.core.sitemap import validate_sitemap_url


class TestValidateSitemapUrl:
    def test_valid_extension_passes(self):
        assert validate_sitemap_url("example.xml")

    def test_invalid_extension_fails(self):
        assert not validate_sitemap_url("example.html")

    def test_no_extension_fails(self):
        assert not validate_sitemap_url("example")

    def test_no_filename_fails(self):
        assert not validate_sitemap_url(".xml")
