from sqlalchemy import extract
from flask import Blueprint, request, jsonify
from extensions import db
from models.billing import Bill
from models.customers import Customer
from models.milk_entry import MilkEntry
from models.payments import Payment

billing = Blueprint("billing", __name__)

# get customer
def get_customer(customer_id):

    return Customer.query.filter_by(
        id=customer_id,
        is_deleted=False
    ).first()

# get milk entries
def get_month_milk_entries(customer_id, bill_month, bill_year):

    return MilkEntry.query.filter(
        MilkEntry.customer_id == customer_id,
        MilkEntry.is_deleted == False,
        extract("month", MilkEntry.entry_date) == bill_month,
        extract("year", MilkEntry.entry_date) == bill_year
    ).all()

# get monthly bill 
def get_bill(customer_id, bill_month, bill_year):

    return Bill.query.filter_by(
        customer_id=customer_id,
        bill_month=bill_month,
        bill_year=bill_year,
        is_deleted=False
    ).first()

# get bill payment
def get_month_payments(customer_id, bill_month, bill_year):

    return Payment.query.filter_by(
        customer_id=customer_id,
        is_deleted=False,
        payment_month=bill_month,
        payment_year=bill_year
    ).all()


# Generate a new bill
@billing.route("/bills/generate", methods=["POST"])
def generate_customer_bill():

    data = request.get_json()

    customer_id = data["customer_id"]
    bill_month = int(data["bill_month"])
    bill_year = int(data["bill_year"])

    customer = get_customer(customer_id)

    if not customer:
        return jsonify({
            "message": "Customer not found"
        }), 404

    if get_bill(customer_id, bill_month, bill_year):
        return jsonify({
            "message": "Bill already generated"
        }), 400

    milk_entries = get_month_milk_entries(
        customer_id,
        bill_month,
        bill_year
    )

    if not milk_entries:
        return jsonify({
            "message": "No milk entries found"
        }), 400

    total_amount = sum(
        float(entry.amount)
        for entry in milk_entries
    )

    payment_entries = get_month_payments(
        customer_id,
        bill_month,
        bill_year
    )

    total_payment = sum(
        float(payment.amount)
        for payment in payment_entries
    )

    last_bill = Bill.query.filter_by(
        customer_id=customer_id,
        is_deleted=False
    ).order_by(
        Bill.bill_year.desc(),
        Bill.bill_month.desc()
    ).first()

    if last_bill:
        current_due = (
            total_amount
            + float(last_bill.current_due)
            - total_payment
        )

    else:
        current_due = (
            total_amount
            - float(customer.opening_balance)
            - total_payment
        )

    bill = Bill(
        customer_id=customer_id,
        total_amount=total_amount,
        total_payment=total_payment,
        current_due=current_due,
        bill_month=bill_month,
        bill_year=bill_year
    )

    db.session.add(bill)
    db.session.commit()

    return jsonify({
        "message": "Bill generated successfully",
        "bill": bill.to_dict()
    }), 201


@billing.route("/bills", methods=["GET"])
def get_bill_entries():

    customer_id = request.args.get("customer_id")
    bill_month = request.args.get("bill_month")
    bill_year = request.args.get("bill_year")

    query = Bill.query.filter_by(
        is_deleted=False
    )

    if customer_id:
        query = query.filter_by(
            customer_id=customer_id
        )

    if bill_month:
        query = query.filter_by(
            bill_month=bill_month
        )

    if bill_year:
        query = query.filter_by(
            bill_year=bill_year
        )

    return jsonify({
        "bill_entries": [
            bill.to_dict()
            for bill in query.all()
        ]
    })

@billing.route("/bills/report", methods=["GET"])
def bill_report():

    customer_id = request.args.get("customer_id")
    bill_month = request.args.get("bill_month")
    bill_year = request.args.get("bill_year")

    if not all([
        customer_id,
        bill_month,
        bill_year
    ]):
        return jsonify({
            "message": "customer_id, bill_month and bill_year are required"
        }), 400

    bill_month = int(bill_month)
    bill_year = int(bill_year)

    customer = get_customer(customer_id)

    if not customer:
        return jsonify({
            "message": "Customer not found"
        }), 404

    bill = get_bill(
        customer_id,
        bill_month,
        bill_year
    )

    if not bill:
        return jsonify({
            "message": "Generate bill first"
        }), 404

    milk_entries = get_month_milk_entries(
        customer_id,
        bill_month,
        bill_year
    )

    payment_entries = get_month_payments(
        customer_id,
        bill_month,
        bill_year
    )

    total_qty = sum(
        float(entry.total_qty)
        for entry in milk_entries
    )

    milk_details = [
        {
            "entry_date": entry.entry_date.strftime("%Y-%m-%d"),
            "morning_qty": float(entry.morning_qty),
            "evening_qty": float(entry.evening_qty),
            "total_qty": float(entry.total_qty),
            "rate": float(entry.rate),
            "amount": float(entry.amount)
        }
        for entry in milk_entries
    ]

    payment_details = [
        {
            "payment_date": payment.payment_date.strftime("%Y-%m-%d"),
            "amount": float(payment.amount)
        }
        for payment in payment_entries
    ]

    return jsonify({

        "customer": {
            "id": customer.id,
            "name": customer.name,
            "opening_balance": customer.opening_balance,
            "mobile": customer.mobile
        },

        "billing_period": {
            "month": bill_month,
            "year": bill_year
        },

        "summary": {
            "total_qty": total_qty,
            "total_amount": float(bill.total_amount),
            "total_payment": float(bill.total_payment),
            "current_due": float(bill.current_due)
        },

        "milk_entries": milk_details,

        "payments": payment_details

    })