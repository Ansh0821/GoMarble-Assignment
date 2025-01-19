import os
from app import create_app  # Import the create_app function
from flask_cors import CORS

app = create_app()  # Create an instance of your Flask app

# Update the CORS configuration to match both frontend and backend
CORS(app, origins=["https://scrapetheweb.netlify.app"])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to port 5000 for local testing
    app.run(host="0.0.0.0", port=port)
