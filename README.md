🌐 Scrape The Web: Review Scraper Platform
Overview
The Review Scraper Platform is a powerful tool that enables users to scrape product reviews from popular e-commerce websites like Amazon and Flipkart. Leveraging OpenAI for dynamic CSS selector identification and Selenium for browser automation, the platform efficiently handles pagination to retrieve all reviews.

The platform consists of:

🖥️ Backend: Implemented in Python using Flask, Selenium, and the OpenAI API.
🎨 Frontend: Built with React, Vite, and TailwindCSS for a responsive and user-friendly interface.
✨ Features
🔍 Dynamic Review Extraction: Extract reviews from Amazon, Flipkart, and other e-commerce websites, even for unsupported sites, using OpenAI-powered dynamic CSS selector identification.
📜 Pagination Handling: Retrieve all reviews across multiple pages automatically.
📊 Responsive Interface: View, interact with, and manage scraped reviews in an intuitive user interface.
🛠️ Customizable Backend: Modify scraping logic for specific websites as needed.
🗂️ Project Structure
Scrape The Web/
├── Backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py
│   ├── utils/
│   │   ├── amazon_scraper.py
│   │   ├── general_scraper.py
│   │   ├── helpers.py
│   │   ├── openai_helper.py
│   ├── main.py
│   ├── requirements.txt
├── Frontend/
│   ├── public/
│   │   ├── index.html
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Homepage.jsx
│   │   │   ├── ScraperPage.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   ├── tailwind.config.js
│   ├── vite.config.js
│   ├── package.json
├── README.md
⚙️ Backend Setup
Requirements
Python 3.8+
Google Chrome browser
Chromedriver
OpenAI API Key
Setup Instructions
Clone the Repository:

bash
Copy code
git clone https://github.com/Ansh0821/GoMarble-Assignment.git
cd GoMarble-Assignment/Backend
Create and Activate a Virtual Environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Add API Keys:

Create a .env file in the Backend directory.
Add the following credentials:
env
Copy code
OPENAI_API_KEY=your_openai_api_key_here
OXYLABS_USERNAME=your_oxylabs_username_here
OXYLABS_PASSWORD=your_oxylabs_password_here
Run the Backend Server:

bash
Copy code
python main.py
API Endpoints:

Endpoint: /api/reviews?page={url}
Description: Extracts reviews from a product URL. Automatically handles pagination and returns structured review data.
🛠️ Dependencies
Flask: For creating API routes.
Selenium: For browser automation to scrape dynamic content.
requests: For handling HTTP requests.
beautifulsoup4: For parsing and navigating HTML content.
trafilatura: For extracting meaningful text from web pages.
openai: For dynamic CSS selector identification using OpenAI API.
pytesseract: For OCR to extract text from images if required.
Pillow: For image processing tasks.
🎨 Frontend Setup
Navigate to the Frontend Directory:

bash
Copy code
cd ../Frontend
Install Dependencies:

bash
Copy code
npm install
Run the Development Server:

bash
Copy code
npm run dev
Access the Frontend:
Open your browser and navigate to http://localhost:3000.

🤝 Contribution
Contributions are welcome! Feel free to fork the repository, create a new branch, and submit a pull request. Please ensure your code follows the existing coding standards and is well-documented. 🚀

🛡️ License
This project is licensed under the MIT License. See the LICENSE file for details.

📧 Contact
If you have any questions or feedback, feel free to reach out at your_email@example.com.

Happy Scraping! 🎉

