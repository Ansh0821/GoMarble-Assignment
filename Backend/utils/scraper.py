from utils.amazon_scraper import process_amazon_reviews
from utils.openai_helper import identify_css_selectors_from_html
from utils.helpers import extract_domain
from utils.general_scraper import extract_reviews as scrape_general_reviews

def process_url(url, pages=1, sort_by="recent"):
    """
    Route the URL to the appropriate scraper based on the domain.
    :param url: The URL of the product page.
    :param pages: Number of pages to scrape (for Amazon-specific use).
    :param sort_by: Sorting preference (for Amazon-specific use).
    :return: The scraped data or error message.
    """
    domain = extract_domain(url)
    if "amazon" in domain:
        return process_amazon_reviews(url, "in", 10, "recent")
    elif "flipkart" in domain:
        return scrape_general_reviews(url)  # Flipkart uses the general scraper now
    else:
        return scrape_general_reviews(url)
