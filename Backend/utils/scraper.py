from utils.amazon_scraper import process_amazon_reviews
from utils.openai_helper import identify_css_selectors_from_html
from utils.helpers import extract_domain
from utils.general_scraper import extract_reviews as scrape_general_reviews

def process_url(url):
    """
    Route the URL to the appropriate scraper based on the domain.
    
    :param url: The URL of the product page.
    :param pages: Number of pages to scrape (default is 1, for Amazon-specific use).
    :param sort_by: Sorting preference (default is "recent", for Amazon-specific use).
    :return: The scraped data or error message.
    """
    # Extract the domain from the given URL
    domain = extract_domain(url)

    # Check if the domain belongs to Amazon
    if "amazon" in domain:
        # Use the Amazon scraper with domain-specific configurations
        return process_amazon_reviews(url, domain="in", pages=10, sort_by="recent")
    
    # Check if the domain belongs to Flipkart
    elif "flipkart" in domain:
        # Use the general scraper for Flipkart
        return scrape_general_reviews(url)
    
    # For any other domain, fallback to the general scraper
    else:
        return scrape_general_reviews(url)
