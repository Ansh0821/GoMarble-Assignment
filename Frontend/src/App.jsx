import { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import HomePage from "./pages/Homepage";
import ScraperPage from "./pages/ScraperPage";
import { HiMenuAlt3, HiX } from "react-icons/hi"; // Icons for Hamburger menu
import "./App.css";

function App() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <Router>
      <div className=" bg-gray-100">
        <nav className="bg-white shadow rounded p-4 flex justify-between items-center">
          <p className="text-green-600 text-2xl font-medium italic">
            ScrapeTheWeb
          </p>

          <div className="md:hidden">
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="text-blue-500 text-3xl focus:outline-none"
            >
              {menuOpen ? <HiX /> : <HiMenuAlt3 />}
            </button>
          </div>


          <ul
            className={`${
              menuOpen ? "block" : "hidden"
            } md:flex md:space-x-4 mt-4 md:mt-0 text-xl`}
          >
            <li>
              <Link
                to="/"
                className="block md:inline text-blue-500 hover:text-blue-700 font-semibold py-1"
                onClick={() => setMenuOpen(false)}
              >
                Home
              </Link>
            </li>
            <li>
              <Link
                to="/scraper"
                className="block md:inline text-blue-500 hover:text-blue-700 font-semibold py-1"
                onClick={() => setMenuOpen(false)}
              >
                Scraper
              </Link>
            </li>
          </ul>
        </nav>

        {/* Content */}
        <div className="p-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/scraper" element={<ScraperPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;