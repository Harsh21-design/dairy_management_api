from flask import Blueprint, request, jsonify
from extensions import db
from models.customers import Customer

customers = Blueprint("customer", __name__)

# Create Customer
@customers.route("/customers", methods=["POST"])
def create_customer():

    data = request.get_json()

    customer = Customer(
        name=data["name"],
        mobile=data["mobile"],
        address=data["address"],
        opening_balance=data["opening_balance"]
    )

    db.session.add(customer)
    db.session.commit()

    return jsonify({
        "message": "Customer created successfully",
        "customer_id": customer.id
    }), 201


# Get All Customers
@customers.route("/customers", methods=["GET"])
def get_customers():

    customers = Customer.query.all()

    result = []

    for customer in customers:
        result.append(customer.to_dict())

    return jsonify(result)


# Get Single Customer
@customers.route("/customers/<int:id>", methods=["GET"])
def get_customer(id):

    customer = Customer.query.get(id)

    if not customer:
        return jsonify({
            "message": "Customer not found"
        }), 404

    return jsonify(customer.to_dict())


# Update Customer
@customers.route("/customers/<int:id>", methods=["PUT"])
def update_customer(id):

    customer = Customer.query.get(id)

    if not customer:
        return jsonify({
            "message": "Customer not found"
        }), 404

    data = request.get_json()

    customer.name = data["name"]
    customer.mobile = data["mobile"]
    customer.address = data["address"]
    customer.opening_balance = data["opening_balance"]

    db.session.commit()

    return jsonify({
        "message": "Customer updated successfully"
    })


# Delete Customer
@customers.route("/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):

    customer = Customer.query.get(id)

    if not customer:
        return jsonify({
            "message": "Customer not found"
        }), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({
        "message": "Customer deleted successfully"
    })