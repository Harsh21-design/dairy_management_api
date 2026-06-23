from flask import request, jsonify, Blueprint
from extensions import db
from datetime import datetime
from sqlalchemy import extract
from models.payments import Payment
from models.customers import Customer
from models.products import Product

payments = Blueprint("payments", __name__)

# add new payment
@payments.route("/payments", methods=["POST"])
def create_payment():

    data = request.get_json()

    customer = Customer.query.filter_by(id=data["customer_id"],is_deleted=False).first()
    
    # check customer
    if not customer:
        return jsonify({
            "message":"customer not found"
        }), 404
    
    product = Product.query.filter_by(id=data["product_id"],is_deleted=False).first()

    #  check product
    if not product:
        return jsonify({
            "message":"product not found"
        }), 404
    
    # check existing payment entry

    existing_payment = Payment.query.filter_by(
        payment_month=extract("month", Payment.payment_date),
        payment_year=extract("year", Payment.payment_date),
        is_deleted=False
    )

    if existing_payment:
        return jsonify({
            "message":"Payment already created"
        })

    # make new payment entry
    payment_date = datetime.strptime(
    data["payment_date"],
    "%Y-%m-%d").date()

    payment_entry = Payment(
       customer_id = data["customer_id"],
       product_id = data["product_id"],
       payment_date = payment_date,
       payment_month = payment_date.month,
       payment_year = payment_date.year,
       amount = data["amount"]
    )

    db.session.add(payment_entry)
    db.session.commit()

    return jsonify({
        "message": "Payment entry created successfully"
    }), 201
    
# Get Payment Entries 
# by Customer ID & Date filter
@payments.route("/payments", methods=["GET"])
def get_payment_entries():
    
    customer_id = request.args.get("customer_id")
    payment_date = request.args.get("payment_date")
    entries = Payment.query.filter_by(is_deleted=False)

    if customer_id:
        entries = entries.filter_by(
            customer_id=customer_id
        )
    
    if payment_date:
        entries = entries.filter_by(
           payment_date=payment_date
        )
    
    payment_entries = entries.all()

    all_entries = []
    for payment_entry in payment_entries:
        all_entries.append(payment_entry.to_dict())
        
    return jsonify({
        "payment_entries": all_entries
    })

# Get Single Payment Entry
@payments.route("/payments/<int:id>", methods=["GET"])
def get_payment_entry(id):

    payment_entry = Payment.query.filter_by(id=id,is_deleted=False).first()

    if not payment_entry:
        return jsonify({
            "message": "Payment Entry not found"
        }), 404

    return jsonify(payment_entry.to_dict())


# Update Payment Entry - Amount
@payments.route("/payments/<int:id>", methods=["PUT"])
def update_payment_entry(id):

    payment_entry = Payment.query.filter_by(id=id,is_deleted=False).first()

    if not payment_entry:
        return jsonify({
            "message": "Payment Entry not found"
        }), 404
    
    data = request.get_json()
    amount = float(data["amount"])

    # updation
    payment_entry.amount = amount

    db.session.commit()

    return jsonify({
        "message": "Payment Entry updated successfully",
        "payment_entry_id": payment_entry.id
    })


# Delete MilkEntry
@payments.route("/payments/<int:id>", methods=["DELETE"])
def delete_payment_entry(id):

    payment_entry = Payment.query.filter_by(id=id,is_deleted=False).first()

    if not payment_entry:
        return jsonify({
            "message": "Payment Entry not found"
        }), 404

    # soft deletion
    payment_entry.is_deleted = True
    db.session.commit()

    return jsonify({
        "message": "Payment Entry deleted successfully",
        "payment_entry_id": payment_entry.id
    })

