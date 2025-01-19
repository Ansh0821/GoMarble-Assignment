import React, { useState } from "react";
import axios from "axios";

const ScraperPage = () => {
  const [url, setUrl] = useState("");
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const reviewsPerPage = 10;
  const API_URL = "http://127.0.0.1:5000";

  const handleScrape = async () => {
    setLoading(true);
    setError("");
    setReviews([]);
    setCurrentPage(1);

    try {
      // Call the API
      const response = await axios.get(`${API_URL}/api/reviews?page=${url}`);
      if (response.data.error) {
        console.error("Backend Error:", response.data.error); // Log the error returned by the backend
        setError(response.data.error); // Display the backend-provided error
      } else if (response.data.reviews && response.data.reviews.length > 0) {
        setReviews(response.data.reviews);
      } else {
        console.error("No reviews fetched for the URL:", url); // Log when no reviews are fetched
        setError("No reviews were fetched. Please try again with a valid URL.");
      }
    } catch (err) {
      // Log the error object for debugging
      console.error("Error fetching reviews:", err);
      
      if (err.response) {
        // If the error is from the API response
        console.error("API Response Error:", err.response.data);
        setError(
          `Error: ${
            err.response.data?.error ||
            "An error occurred while scraping reviews. Please try again."
          }`
        );
      } else if (err.request) {
        // If no response was received
        console.error("No response received from the backend:", err.request);
        setError("No response from the server. Please check your connection.");
      } else {
        // Any other errors
        console.error("Error during the request setup:", err.message);
        setError("An unexpected error occurred. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const paginatedReviews = reviews.slice(
    (currentPage - 1) * reviewsPerPage,
    currentPage * reviewsPerPage
  );

  const totalPages = Math.ceil(reviews.length / reviewsPerPage);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl md:text-3xl font-bold mb-4 text-center">
        Scrape Product Reviews
      </h1>

      <p className="mb-4 text-sm md:text-base">
        <strong>Instructions:</strong>
        <br />
        Enter the URL of the product or review page to scrape reviews. Below are examples for supported websites:
        <ul className="list-disc ml-6 mt-2">
          <li>
            <strong>Amazon:</strong> Provide the product page URL (e.g., 
            <code className="bg-gray-200 px-1">https://www.amazon.in/dp/B08L5WHFT9</code>)
          </li>
          <li>
            <strong>Flipkart:</strong> Provide the product reviews page URL (e.g., 
            <code className="bg-gray-200 px-1">https://www.flipkart.com/product-reviews/itm12345abcde</code>)
          </li>
          <li>
            <strong>Other Websites:</strong> Provide the product page or review page URL (e.g., Shopify, eBay). 
            OpenAI will try to identify the review structure automatically.
          </li>
        </ul>
      </p>

      <div className="mb-6 flex flex-col sm:flex-row items-center">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter the product or review page URL"
          className="border border-gray-300 rounded-lg px-4 py-2 w-full sm:w-3/4 mb-4 sm:mb-0 sm:mr-4"
        />
        <button
          onClick={handleScrape}
          disabled={!url || loading}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg w-full sm:w-1/4"
        >
          {loading ? "Scraping..." : "Scrape Reviews"}
        </button>
      </div>

      {loading && (
        <div className="flex justify-center items-center mt-4">
          <div className="loader border-t-4 border-blue-500 rounded-full w-16 h-16 animate-spin"></div>
          <p className="ml-4">Fetching reviews. Please wait...</p>
        </div>
      )}

      {error && (
        <div className="mt-4 p-4 bg-red-100 text-red-700 border border-red-400 rounded-lg text-center">
          <strong>Error:</strong> {error}
        </div>
      )}

      {reviews.length > 0 && (
        <div className="mt-6">
          <h2 className="text-xl md:text-2xl font-bold mb-4 text-center">
            Total Reviews Scraped: {reviews.length}
          </h2>
          <ul className="space-y-4">
            {paginatedReviews.map((review, index) => (
              <li
                key={index}
                className="border border-gray-300 rounded-lg p-4 bg-white shadow-sm"
              >
                <p className="text-sm md:text-base">
                  <strong>Title:</strong> {review.title || "No title"}
                </p>
                <p className="text-sm md:text-base">
                  <strong>Body:</strong> {review.body || "No content"}
                </p>
                <p className="text-sm md:text-base">
                  <strong>Rating:</strong> {review.rating || "No rating"}
                </p>
                <p className="text-sm md:text-base">
                  <strong>Reviewer:</strong> {review.reviewer || "Anonymous"}
                </p>
              </li>
            ))}
          </ul>
          <div className="mt-4 flex flex-wrap justify-center">
            {Array.from({ length: totalPages }, (_, i) => (
              <button
                key={i + 1}
                onClick={() => handlePageChange(i + 1)}
                className={`px-4 py-2 mx-1 mb-2 border rounded ${
                  currentPage === i + 1
                    ? "bg-blue-500 text-white"
                    : "bg-white text-blue-500 border-blue-500"
                }`}
              >
                {i + 1}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ScraperPage;
