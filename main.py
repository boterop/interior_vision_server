import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from waitress import serve
from routes.ai import ai
from routes.ai_test import ai_test

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(ai)
app.register_blueprint(ai_test)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=os.getenv("PORT", 6000))
