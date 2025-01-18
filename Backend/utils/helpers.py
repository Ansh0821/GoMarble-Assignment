import re
from urllib.parse import urlparse

def extract_domain(url):
    """
    Extract the domain from a URL.
    :param url: Full URL.
    :return: The domain as a string.
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc

def extract_asin(url):
    """
    Extract the ASIN from an Amazon product URL.
    :param url: The Amazon product page URL.
    :return: The ASIN as a string or None if not found.
    """
    match = re.search(r"/([A-Z0-9]{10})(?:[/?]|$)", url)
    return match.group(1) if match else None
