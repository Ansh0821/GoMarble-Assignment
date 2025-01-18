import React from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
  return (
    <div className="bg-white shadow rounded p-6 max-w-3xl mx-auto mt-10 text-center">
      <h1 className="text-4xl font-bold mb-6 text-green-600">Welcome to ScrapeTheWeb</h1>
      <p className="text-gray-700 text-lg mb-4">
        ScrapeTheWeb is a powerful platform designed to help you extract reviews from product pages of popular e-commerce websites like Amazon, Flipkart, and many more. Whether you're researching products, analyzing customer feedback, or just curious, we've got you covered.
      </p>
      <p className="text-gray-700 text-lg mb-6">
        Simply provide the URL of the product or review page, and let our advanced technology do the work for you. Extract detailed reviews, ratings, and more in seconds.
      </p>
      <Link
        to="/scraper"
        className="px-6 py-3 bg-blue-500 text-white rounded-lg text-lg font-semibold hover:bg-blue-600 transition duration-200"
      >
        Get Started
      </Link>
    </div>
  );
};

export default HomePage;
