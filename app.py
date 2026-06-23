import os
from flask import Flask
from extensions import db
from dotenv import load_dotenv
from routes.customer_routes import customers
from routes.products_routes import products
from routes.milk_entry_routes import milk_entries
from routes.daily_entry_route import daily_entries
from routes.payment_routes import payments
from routes.billing_routes import billing

load_dotenv()   
app = Flask(__name__)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
# Initialize Database
db.init_app(app)

# Register Blueprint
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


