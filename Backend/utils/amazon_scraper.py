import requests
from utils.helpers import extract_asin
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv()
OXYLABS_USERNAME = os.getenv("OXYLABS_USERNAME")
OXYLABS_PASSWORD = os.getenv("OXYLABS_PASSWORD")

def process_amazon_reviews(url, domain, pages, sort_by):
    """
    Fetch reviews for an Amazon product using Oxylabs API.
    :param url: Amazon product page URL
    :param domain: Amazon domain (e.g., 'com', 'in', etc.)
    :param pages: Number of review pages to scrape
    :param sort_by: Sort reviews by 'recent' or 'top'
    :return: JSON response with reviews
    """
    asin = extract_asin(url)  # Extract ASIN from the given URL
    if not asin:
        return {"error": "Unable to extract ASIN from URL"}

    # Build the payload for the Oxylabs API
    payload = {
        'source': 'amazon_reviews',
        'domain': domain,
        'query': asin,
        'pages': pages,
        'parse': True,
        'context': [
            {
                "key": "sort_by",
                "value": sort_by
            }
        ]
    }

    try:
        response = requests.post(
            'https://realtime.oxylabs.io/v1/queries',
            auth=(OXYLABS_USERNAME, OXYLABS_PASSWORD),
            json=payload
        )
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        pprint(data)  # Debugging purpose

        # Extract reviews
        reviews = []
        for result in data.get("results", []):
            content = result.get("content", {})
            reviews.extend(content.get("reviews", []))

        return {"reviews": reviews, "reviews_count": len(reviews)}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
