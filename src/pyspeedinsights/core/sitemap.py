import xml.etree.ElementTree as ET

import requests

from pyspeedinsights.api.request import url_validator


def request_sitemap(url):
    url = url_validator(url)
    
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
    root = ET.fromstring(sitemap)
    namespace = '{http://www.sitemaps.org/schemas/sitemap/0.9}'

    urls = []
    for url in root.findall(f'{namespace}url'):
        loc = url.find(f'{namespace}loc')
        urls.append(loc.text)
        
    return urls