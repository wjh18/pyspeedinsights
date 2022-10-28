import xml.etree.ElementTree as ET
from os.path import splitext
from urllib.parse import urlsplit

import requests

from ..utils.urls import validate_url


def request_sitemap(url):
    """Retrieve the sitemap from the URL provided in cmd args."""

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


def parse_sitemap(sitemap):
    """Parse URLs from the XML sitemap and return a list of URLs."""

    print("Parsing URLs from sitemap...")

    root = ET.fromstring(sitemap)
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"

    urls = []
    for url in root.findall(f"{namespace}url"):
        loc = url.find(f"{namespace}loc")
        urls.append(loc.text)

    return urls


def validate_sitemap_url(url):
    """Validate that the sitemap URL is valid (.xml format)."""

    u = urlsplit(url)
    ext = splitext(u.path)[1]
    return ext == ".xml"
