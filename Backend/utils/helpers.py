import re
from urllib.parse import urlparse

def extract_domain(url):
    """
    Extract the domain from a given URL.
    
    Example:
        Input: "https://www.amazon.com/product/12345"
        Output: "www.amazon.com"
    
    :param url: Full URL as a string.
    :return: The domain as a string.
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc


def extract_asin(url):
    """
    Extract the ASIN (Amazon Standard Identification Number) from an Amazon product URL.
    
    Example:
        Input: "https://www.amazon.com/dp/B08N5WRWNW"
        Output: "B08N5WRWNW"

    :param url: The Amazon product page URL.
    :return: The ASIN as a string or None if not found.
    """
    match = re.search(r"/([A-Z0-9]{10})(?:[/?]|$)", url)
    return match.group(1) if match else None
