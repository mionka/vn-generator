from urllib.parse import urlparse


def get_hostname(url: str) -> str:
    """Extracts and returns the hostname from a given URL."""
    return urlparse(url).netloc
