import os
from flask import Flask
from flask_cors import CORS
from extensions import db, jwt
from dotenv import load_dotenv
from config import Config
from routes.auth_routes import auth
from routes.customer_routes import customers
from routes.products_routes import products
from routes.milk_entry_routes import milk_entries
from routes.daily_entry_route import daily_entries
from routes.payment_routes import payments
from routes.billing_routes import billing
from models.users import User

load_dotenv()   
app = Flask(__name__)
CORS(app)

# Database Configuration
app.config.from_object(Config)

# Initialize Database & JWT
db.init_app(app)
jwt.init_app(app)

# Register Blueprint
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
        "message": "Welcome to Dairy Management API"
    }

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)


