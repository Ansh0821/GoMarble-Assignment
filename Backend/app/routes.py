from flask import Blueprint, request, jsonify
from utils.scraper import extract_reviews

review_routes = Blueprint("review_routes", __name__)

@review_routes.route("/api/reviews", methods=["GET"])
def get_reviews():
    url = request.args.get("page")
    if not url:
        return jsonify({"error": "Missing 'page' parameter in the request"}), 400

    try:
        # Call the extract_reviews function
        reviews_data = extract_reviews(url)
        return jsonify(reviews_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
