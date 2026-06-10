import os
from flask import Flask
from extensions import db
from dotenv import load_dotenv
from routes.customer_routes import customers
from models.customers import Customer
from config import Config


load_dotenv()   
app = Flask(__name__)

# Database Configuration
app.config.from_object(Config)

# Initialize Database
db.init_app(app)

# Register Blueprint
app.register_blueprint(customers)

@app.route("/")
def home():
    return {
        "message": "Welcome to Dairy Management API"
    }

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)