import os
from app import create_app  # Import the create_app function

app = create_app()  # Create an instance of your Flask app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to port 5000 for local testing
    app.run(host="0.0.0.0", port=port)
