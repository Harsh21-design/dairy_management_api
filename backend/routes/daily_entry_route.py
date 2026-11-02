from flask import request, jsonify, Blueprint
from models.milk_entry import MilkEntry

daily_entries = Blueprint("daily_entries", __name__)

@daily_entries.route("/daily-entries", methods=["GET"])
def get_daily_entries():

    entry_date = request.args.get("date")

    if not entry_date:
        return jsonify({
            "message": "Date is required"
        }), 400

    entries = MilkEntry.query.filter_by(
        entry_date=entry_date,
        is_deleted=False
    ).all()

    if not entries:
        return jsonify({
            "message":"No Entries are found"
        })

    result = []

    for entry in entries:
        result.append({
            "customer_name": entry.customer.name,
            "morning_qty": float(entry.morning_qty),
            "evening_qty": float(entry.evening_qty),
            "total_qty": float(entry.total_qty),
            "rate": float(entry.rate),
            "amount": float(entry.amount)
    })

    return jsonify({
        "date": entry_date,
        "total_entries": len(result),
        "entries": result
    })