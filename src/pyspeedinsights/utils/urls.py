from urllib.parse import urlsplit


def validate_url(url):
    """
    Adds a scheme to the URL if missing and
    validates that the URL is fully qualified (not just a path).
    """

    err = "Invalid URL. Please enter a valid Fully-Qualified Domain Name (FQDN)."
    u = urlsplit(url)

    if not (u.scheme and u.netloc):
        if "." not in u.path:
            raise SystemExit(err)
        u = u._replace(scheme="https", netloc=u.path, path="")

    return u.geturl()
