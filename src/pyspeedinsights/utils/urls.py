from urllib.parse import urlsplit


def validate_url(url):
    """
    Adds a scheme to the URL if missing and
    validates that the URL is fully qualified (not just a path).
    """

    err = "Invalid URL. Please enter a valid Fully-Qualified Domain Name (FQDN)."
    replacements = {}
    u = urlsplit(url)

    if not u.scheme:
        replacements["scheme"] = "https"

    if not u.netloc:
        if ("." not in u.path) or ("." and "/" in u.path):
            raise SystemExit(err)
        else:
            replacements["netloc"] = u.path
            replacements["path"] = ""

    replacements["fragment"] = ""
    replacements["query"] = ""
    u = u._replace(**replacements)

    return u.geturl()
