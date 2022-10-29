import xml.etree.ElementTree as ET
from os.path import splitext
from urllib.parse import urlsplit

import requests

from ..utils.urls import validate_url


def request_sitemap(url):
    """Retrieve the sitemap from the given URL"""

    url = validate_url(url)
    # Set a dummy user agent to avoid bot detection by firewalls
    # e.g. CloudFlare issues a 403 if it detects the default requests module user-agent
    dummy_user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/104.0.5112.79 Safari/537.36"
    )
    headers = {"user-agent": dummy_user_agent}

    if not validate_sitemap_url(url):
        err = (
            "Invalid sitemap URL provided. Please provide a URL to a valid XML sitemap."
        )
        raise SystemExit(err)
    try:
        print(f"Requesting sitemap... ({url})")
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        raise SystemExit(errh)
    except requests.exceptions.ConnectionError as errc:
        raise SystemExit(errc)
    except requests.exceptions.Timeout as errt:
        raise SystemExit(errt)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    sitemap = resp.text
    print("Sitemap retrieval successful!")

    return sitemap


def validate_sitemap_url(url):
    """Validate that the sitemap URL is valid (.xml format)."""

    u = urlsplit(url)
    ext = splitext(u.path)[-1]
    return ext == ".xml"


def process_sitemap(sitemap):
    """
    Process an individual sitemap or recursively process multiple sitemaps
    via a sitemap index and return a full list of request URLs.
    """

    root = ET.fromstring(sitemap)
    sitemap_type = root.tag.split("}")[-1]

    if sitemap_type == "sitemapindex":
        request_urls = []
        sitemap_urls = _parse_sitemap_index(root)

        for sm_url in sitemap_urls:
            sitemap = request_sitemap(sm_url)
            request_urls.extend(process_sitemap(sitemap))

    elif sitemap_type == "urlset":
        request_urls = _parse_sitemap_urls(root)

    return request_urls


def _parse_sitemap_index(root):
    """Parse sitemap URLs from the sitemap index and return them as a list."""

    print("Sitemap index found. Parsing sitemap URLs...")
    return _parse_urls_from_root(root, type="sitemap")


def _parse_sitemap_urls(root):
    """Parse URLs from the XML sitemap and return a list of request URLs."""

    print("Parsing URLs from sitemap...")
    return _parse_urls_from_root(root)


def _parse_urls_from_root(root, type="url"):
    """Parse URL locs from root xml element"""

    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    urls = []

    for el in root.findall(f"{namespace}{type}"):
        loc = el.find(f"{namespace}loc")
        urls.append(loc.text)

    return urls
