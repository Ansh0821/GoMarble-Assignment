from flask import Flask
from app.routes import review_routes

app = Flask(__name__)

# Register routes
app.register_blueprint(review_routes)

if __name__ == "__main__":
    app.run(debug=True)
