from flask import Blueprint, request, jsonify
from extensions import db
from models.billing import Bill
from models.customers import Customer
from models.milk_entry import MilkEntry
from models.payments import Payment

billing = Blueprint("billing", __name__)

# Generate Monthly Bill
@billing.route("/bills/generate", methods=["POST"])
def generate_customer_bill():
    
    data = request.get_json()

    customer_id = data["customer_id"]
    bill_month = int(data["bill_month"])
    bill_year = int(data["bill_year"])

    # Check Customer
    customer = Customer.query.filter_by(
        id=customer_id,
        is_deleted=False
    ).first()

    if not customer:
        return jsonify({
            "message": "Customer not found"
        }), 404

    # Check Existing Bill
    existing_bill = Bill.query.filter_by(
        customer_id=customer_id,
        bill_month=bill_month,
        bill_year=bill_year,
        is_deleted=False
    ).first()

    if existing_bill:
        return jsonify({
            "message": "Bill already generated"
        }), 400

    # Get Milk Entries
    milk_entries = MilkEntry.query.filter_by(
        customer_id=customer_id,
        is_deleted=False
    ).all()

    # Calculate Total Milk Amount
    total_amount = 0

    for entry in milk_entries:

        if (
            entry.entry_date.month == bill_month
            and
            entry.entry_date.year == bill_year
        ):
            total_amount += float(entry.amount)
    
    if total_amount == 0:
        return jsonify({
            "message": "No milk entries found for this month"
        }), 400
    
    # get total payment 
    payment_entries = Payment.query.filter_by(
        customer_id=customer_id,
        is_deleted=False
    ).all()

    total_payment = 0
    
    for payment in payment_entries:
    
        if (
            payment.payment_date.month == bill_month
            and
            payment.payment_date.year == bill_year
        ):
            total_payment += float(payment.amount)

    # Previous Due Logic
    last_bill = Bill.query.filter_by(
        customer_id=customer_id,
        is_deleted=False
    ).order_by(Bill.bill_year.desc(),
               Bill.bill_month.desc()).first()

    if last_bill:
        previous_due = float(last_bill.current_due)
        # Current Due
        current_due = total_amount + previous_due - total_payment

    else:
        previous_due = float(customer.opening_balance)
        # Current Due
        current_due = total_amount - previous_due - total_payment

    # Create Bill
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
        "message": "Bill generated successfully"
    }), 201

# get bill
@billing.route("/bills", methods=["GET"])
def get_bill_entries():
    
    customer_id = request.args.get("customer_id")
    bill_month = request.args.get("bill_month")
    bill_year = request.args.get("bill_year")

    entries = Bill.query.filter_by(is_deleted=False)

    if customer_id:
        entries = entries.filter_by(
            customer_id=customer_id
        )
    if bill_month:
        entries = entries.filter_by(
            bill_month=bill_month
        )
    if bill_year:
        entries = entries.filter_by(
            bill_year=bill_year
        )
   
    bill_entries = entries.all()

    all_entries = []
    for bill_entry in bill_entries:
        all_entries.append(bill_entry.to_dict())
        
    return jsonify({
        "bill_entries": all_entries
    })

# BILL REPORT
@billing.route("/bills/report", methods=["GET"])
def bill_report():

    customer_id = request.args.get("customer_id")
    bill_month = request.args.get("bill_month")
    bill_year = request.args.get("bill_year")

    if not customer_id and not bill_month and not bill_year:
        return jsonify({
            "message": "customer_id, bill_month and bill_year are required"
        }), 400

    bill_month = int(bill_month)
    bill_year = int(bill_year)

    # Check Customer
    customer = Customer.query.filter_by(
        id=customer_id,
        is_deleted=False
    ).first()

    if not customer:
        return jsonify({
            "message": "Customer not found"
        }), 404

    # Get Bill
    bill = Bill.query.filter_by(
        customer_id=customer_id,
        bill_month=bill_month,
        bill_year=bill_year,
        is_deleted=False
    ).first()

    if not bill:
        return jsonify({
            "message": "Bill not generated\nGenerate bill first"
        }), 404

    # Milk Entries
    milk_entries = MilkEntry.query.filter_by(
        customer_id=customer_id,
        is_deleted=False
    ).all()

    if not milk_entries:
        return jsonify({
            "message": "No Milk Entries Created"
        }), 404

    milk_details = []
    total_qty = 0

    for entry in milk_entries:

        if (
            entry.entry_date.month == bill_month
            and
            entry.entry_date.year == bill_year
        ):

            total_qty += float(entry.total_qty)

            milk_details.append({
                "entry_date": entry.entry_date.strftime("%Y-%m-%d"),
                "morning_qty": float(entry.morning_qty),
                "evening_qty": float(entry.evening_qty),
                "total_qty": float(entry.total_qty),
                "rate": float(entry.rate),
                "amount": float(entry.amount)
            })

    # Payments
    payment_entries = Payment.query.filter_by(
        customer_id=customer_id,
        is_deleted=False
    ).all()

    payment_details = []

    for payment in payment_entries:

        if (
            payment.payment_date.month == bill_month
            and
            payment.payment_date.year == bill_year
        ):

            payment_details.append({
                "payment_date": payment.payment_date.strftime("%Y-%m-%d"),
                "amount": float(payment.amount)
            })

    return jsonify({

        "customer": {
            "id": customer.id,
            "name": customer.name,
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
