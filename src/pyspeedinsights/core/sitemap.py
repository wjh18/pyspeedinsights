"""Requesting and parsing of sitemaps to obtain request URLs for API calls.

Includes support for recursive parsing of multiple sitemaps via a sitemap index.
"""

import xml.etree.ElementTree as ET
from os.path import splitext
from typing import Optional
from urllib.parse import urlsplit

import requests

from ..utils.urls import validate_url


def request_sitemap(url: str) -> str:
    """Retrieves the sitemap from the given URL.

    Validates the url format and whether the url is a valid sitemap.
    Makes a get request to retrieve the sitemap content in XML format.

    Returns:
        A str with XML sitemap text content.
    Raises:
        SystemExit: The sitemap URL is invalid or a request failed.
    """
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
        raise SystemExit(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        raise SystemExit(f"Connection Error: {errc}")
    except requests.exceptions.Timeout as errt:
        raise SystemExit(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        raise SystemExit(f"Request Error: {err}")

    sitemap = resp.text
    print("Sitemap retrieval successful!")
    return sitemap


def validate_sitemap_url(url: str) -> bool:
    """Checks that the sitemap URL is valid (.xml format)."""
    u = urlsplit(url)
    ext = splitext(u.path)[-1]
    return ext == ".xml"


def get_sitemap_root(sitemap: str) -> ET.Element:
    """Gets the root element of the sitemap."""
    return ET.fromstring(sitemap)


def get_sitemap_type(root: ET.Element) -> str:
    """Gets the tag value of the root element to determine sitemap type."""
    return root.tag.split("}")[-1]


def process_sitemap(sitemap: str) -> list[Optional[str]]:
    """Processes a sitemap or sitemap index based on type.

    Multiple sitemaps are processed recursively via a sitemap index.

    Returns:
        A full list of request URLs for use in requests.
    Raises:
        SystemExit: The sitemap type couldn't be parsed from the root element.
                    The sitemap type parsed from the root element is invalid.
                    No URLs were parsed from the sitemap(s) successfully.
    """
    err = "Sitemap format invalid."

    try:
        root = get_sitemap_root(sitemap)
        sitemap_type = get_sitemap_type(root)
    except ET.ParseError:
        raise SystemExit(err)

    if sitemap_type == "sitemapindex":
        request_urls = []
        sitemap_urls = _parse_sitemap_index(root)
        for sm_url in sitemap_urls:
            if sm_url is not None:
                sitemap = request_sitemap(sm_url)
                request_urls.extend(process_sitemap(sitemap))
    elif sitemap_type == "urlset":
        request_urls = _parse_sitemap_urls(root)
    else:
        raise SystemExit(err)

    if not request_urls:
        raise SystemExit("No URLs found in the sitemap(s).")
    return request_urls


def _parse_sitemap_index(root: ET.Element) -> list[Optional[str]]:
    """Parse sitemap URLs from the sitemap index and return them as a list."""
    print("Sitemap index found. Parsing sitemap URLs...")
    return _parse_urls_from_root(root, type="sitemap")


def _parse_sitemap_urls(root: ET.Element) -> list[Optional[str]]:
    """Parse URLs from the XML sitemap and return a list of request URLs."""
    print("Parsing URLs from sitemap...")
    return _parse_urls_from_root(root)


def _parse_urls_from_root(root: ET.Element, type: str = "url") -> list[Optional[str]]:
    """Parse URL locs from root xml element."""
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    urls = []
    for el in root.findall(f"{namespace}{type}"):
        loc = el.find(f"{namespace}loc")
        if loc is not None:
            urls.append(loc.text)
    return urls
