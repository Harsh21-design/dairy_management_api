import os
import sys

# Ensure backend directory and project root are in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(1, ROOT_DIR)

from flask import Flask
from flask_cors import CORS
from extensions import db, jwt
from config import Config
from routes.auth_routes import auth
from routes.customer_routes import customers
from routes.products_routes import products
from routes.milk_entry_routes import milk_entries
from routes.daily_entry_route import daily_entries
from routes.payment_routes import payments
from routes.billing_routes import billing
from models.users import User

app = Flask(__name__)
CORS(app)

# Database & JWT Configuration
app.config.from_object(Config)

# Initialize Database & JWT
db.init_app(app)
jwt.init_app(app)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(customers)
app.register_blueprint(products)
app.register_blueprint(milk_entries)
app.register_blueprint(daily_entries)
app.register_blueprint(payments)
app.register_blueprint(billing)

@app.route("/")
def home():
    return {
        "status": "online",
        "service": "Dairy Management API",
        "version": "2.0.0"
    }

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)

