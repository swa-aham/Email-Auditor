from flask import Flask
from flask_cors import CORS
from src.routes import setup_routes

app = Flask(__name__)
CORS(app)

setup_routes(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
