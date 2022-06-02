import xml.etree.ElementTree as ET
from urllib.parse import urlsplit
from os.path import splitext

import requests

from pyspeedinsights.api.request import validate_url


def request_sitemap(url):
    """
    Get sitemap from URL provided in cmd args.
    """
    url = validate_url(url)
    
    if validate_sitemap_url(url) != True:
        err = "Invalid sitemap provided. Please provide a link to a valid XML sitemap."
        raise SystemExit(err)
    try:
        resp = requests.get(url)
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
    return sitemap

    
def parse_sitemap(sitemap):
    """
    Parse URLs from XML sitemap and return a list of them.
    """
    root = ET.fromstring(sitemap)
    namespace = '{http://www.sitemaps.org/schemas/sitemap/0.9}'

    urls = []
    for url in root.findall(f'{namespace}url'):
        loc = url.find(f'{namespace}loc')
        urls.append(loc.text)
        
    return urls


def validate_sitemap_url(url):
    """
    Validate that the sitemap URL is in .xml format.
    """
    u = urlsplit(url)
    ext = splitext(u.path)[1]
    if ext == '.xml':
        return True