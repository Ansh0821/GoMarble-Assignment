from flask import Blueprint, request, jsonify
from utils.scraper import process_url

review_routes = Blueprint("review_routes", __name__)

@review_routes.route("/api/reviews", methods=["GET"])
def get_reviews():
    """
    API endpoint to scrape reviews from a product page.
    Expects 'page' as a query parameter.
    """
    # Fetch 'page' query parameter
    url = request.args.get("page")
    if not url:
        return jsonify({"error": "Missing 'page' query parameter in the URL"}), 400

    # Process the URL based on domain (Amazon, Flipkart, etc.)
    result = process_url(url)
    return jsonify(result)
