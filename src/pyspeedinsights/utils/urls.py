"""Utilities for URL processing."""

import logging
from urllib.parse import urlsplit

logger = logging.getLogger(__name__)


class InvalidURLError(Exception):
    """A base exception for an invalid URL format."""


def validate_url(url: str) -> str:
    """Checks that a URL is valid and fully-qualified.

    Adds a scheme to the URL if missing.
    The hostname is stored in u.path instead of u.netloc when the URL str has no path.
    In this scenario, checking the u.path is necessary to ensure the URL has a domain
    and the path doesn't precede the hostname (e.g. path/example.com).

    Returns:
        The sanitized URL as a str.
    Raises:
        InvalidURLError: The user entered a URL without a path that has no domain
        or a URL whose path precedes the hostname (e.g. path/example.com).
    """
    logger.info("Checking if request URL is a valid URL.")
    err = "Invalid URL. Please enter a valid fully-qualified URL."

    replacements = {}
    u = urlsplit(url)

    if not u.scheme:
        replacements["scheme"] = "https"
    if not u.netloc:
        p_sep, dot = u.path.find("/"), u.path.find(".")
        path_before_host = p_sep < dot and p_sep > 0
        no_host = "." not in u.path
        if path_before_host or no_host:
            raise InvalidURLError(err)  # Logged as CRITICAL in main()
        else:
            replacements["netloc"] = u.path
            replacements["path"] = ""
    elif "." not in u.netloc:
        # URLs with schemes but no TLD
        raise InvalidURLError(err)  # Logged as CRITICAL in main()

    replacements["fragment"] = ""
    replacements["query"] = ""
    u = u._replace(**replacements)
    return u.geturl()
