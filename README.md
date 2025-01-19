# 🌐 Scrape The Web: Review Scraper Platform

## Overview
The **Review Scraper Platform** is a powerful tool that enables users to scrape product reviews from popular e-commerce websites like **Amazon** and **Flipkart**. Leveraging **OpenAI** for dynamic CSS selector identification and **Selenium** for browser automation, the platform efficiently handles pagination to retrieve all reviews.

The platform consists of:
- 🖥️ **Backend**: Implemented in Python using **Flask**, **Selenium**, and the **OpenAI API**.
- 🎨 **Frontend**: Built with **React**, **Vite**, and **TailwindCSS** for a responsive and user-friendly interface.

---

## ✨ Features
- 🔍 **Dynamic Review Extraction**: Extract reviews from Amazon, Flipkart, and other e-commerce websites, even for unsupported sites, using OpenAI-powered dynamic CSS selector identification.
- 📜 **Pagination Handling**: Retrieve all reviews across multiple pages automatically.
- 📊 **Responsive Interface**: View, interact with, and manage scraped reviews in an intuitive user interface.
- 🛠️ **Customizable Backend**: Modify scraping logic for specific websites as needed.

---

## 🗂️ Project Structure
Scrape The Web/
├── Backend/
│ ├── app/
│ │ ├── init.py
│ │ ├── routes.py
│ ├── utils/
│ │ ├── amazon_scraper.py
│ │ ├── general_scraper.py
│ │ ├── helpers.py
│ │ ├── openai_helper.py
│ ├── main.py
│ ├── requirements.txt
├── Frontend/
│ ├── public/
│ │ ├── index.html
│ ├── src/
│ │ ├── pages/
│ │ │ ├── Homepage.jsx
│ │ │ ├── ScraperPage.jsx
│ │ ├── App.jsx
│ │ ├── App.css
│ ├── tailwind.config.js
│ ├── vite.config.js
│ ├── package.json
├── README.md


---

## ⚙️ Backend Setup

### Requirements
- Python **3.8+**
- **Google Chrome** browser
- **Chromedriver**
- OpenAI API Key

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Ansh0821/GoMarble-Assignment.git
   cd GoMarble-Assignment/Backend

2. **Create and Activate a virtual environment**:
   - On macOS/Linux:
      ```bash
      python -m venv venv
      source venv/bin/activate
   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate

3. **Install Dependencies**:
   ```bash
      pip install -r requirements.txt

4. **Add API Keys**:
   - Create a `.env` file in the `Backend` directory
   - Add the following credentials:
     ```bash
     OPENAI_API_KEY=<api_key>
      OXYLABS_USERNAME=Ansh_2108_sqYtX
      OXYLABS_PASSWORD=pCFt33EVA7Gsn9q_

5. **Run the Backend server**:
   -**Endpoint**:`api/reviews?page={url}`
      - **Description**: Extracts reviews from a product URL. Automatically handles pagination and returns structured review data.
  
## 🛠️ Dependencies

- **Flask**: For creating API routes.
- **Selenium**: For browser automation to scrape dynamic content.
- **requests**: For handling HTTP requests.
- **beautifulsoup4**: For parsing and navigating HTML content.
- **openai**: For dynamic CSS selector identification using OpenAI API.
- **python-dotenv**: For managing environment variables.
- **webdriver_manager**: For managing ChromeDriver automatically.

---

---

## 🎨 Frontend Setup

### Requirements
- Node.js **14+**
- npm

### Setup Instructions

1. **Navigate to the Frontend Directory**:
   ```bash
   cd GoMarble-Assignment/Frontend

### Install Dependencies:
```bash
npm install
```

### Run the Frontend:
```bash
npm run dev
```

### Access the Application:
Open your browser and navigate to:
[http://localhost:5173](http://localhost:5173)

--

## 🌐 Deployment
The project has been deployed and can be accessed via the following URLs:
- **Backend**: [https://scrape-the-web-backend.onrender.com](https://scrape-the-web-backend.onrender.com)


For any updates or issues with the deployed application, ensure the backend environment variables are properly configured via the Render dashboard.

## 💡 Notes

### For OpenAI Quota and testing
If reviews are not being fetched on the deployed server, it might be due to the OpenAI quota being exceeded. 

In such cases:
- Please test the application locally by running the backend server on your local machine.
- Ensure that the **OPENAI_API_KEY** in your `.env` file is valid and has sufficient quota.

To test locally, follow the backend setup instructions provided above.

- Ensure the .env file is properly configured with valid API keys.
- For unsupported websites, the OpenAI API dynamically identifies the CSS selectors to scrape reviews.

  ## 🚀 Usage
  - Access the deployed frontend to interact with the review scraper.
  - Provide product URLs for Amazon, Flipkart, or other e-commerce platforms.
  - View extracted reviews directly in the interface.
