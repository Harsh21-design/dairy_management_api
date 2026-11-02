from flask import Blueprint, request, jsonify
from extensions import db
from models.milk_entry import MilkEntry
from models.customers import Customer
from models.products import Product

milk_entries = Blueprint("milk_entries", __name__)

# Create Milk Entry
@milk_entries.route("/milk-entries",methods=["POST"])
def create_milk_entry():

    data = request.get_json()

    customer = Customer.query.filter_by(id=data["customer_id"],is_deleted=False).first()

    if not customer:
        return jsonify({
            "message":"customer not found"
        }), 404
    
    product = Product.query.filter_by(id=data["product_id"],is_deleted=False).first()

    if not product:
        return jsonify({
            "message":"product not found"
        }), 404
    
    # check duplicate customer entry for same date
    existing_entry = MilkEntry.query.filter_by(
        customer_id = data["customer_id"],
        entry_date = data["entry_date"],
        is_deleted=False
    ).first()

    if existing_entry:
        return jsonify({
            "message":"Entry already exists for customer"
        })
    
    morning_qty = float(data.get("morning_qty", 0))
    evening_qty = float(data.get("evening_qty", 0))

    total_qty = morning_qty + evening_qty

    rate = float(product.rate)

    amount = total_qty * rate

    milk_entry = MilkEntry(
       customer_id = data["customer_id"],
       product_id = data["product_id"],
       entry_date = data["entry_date"],

       morning_qty = morning_qty,
       evening_qty = evening_qty,

       total_qty = total_qty,
       rate = rate,
       amount = amount
  
    )

    db.session.add(milk_entry)
    db.session.commit()

    return jsonify({
        "message": "Milk entry created successfully",
        "milk_entry_id": milk_entry.id
    }), 201


# # Get All Milk Entries
# @milk_entries.route("/milk-entries", methods=["GET"])
# def get_milk_entries():

#     milk_entries = MilkEntry.query.filter_by(is_deleted=False).all()

#     result = []

#     for milk_entry in milk_entries:
#         result.append(milk_entry.to_dict())

#     if not result:
#         return jsonify({
#             "message": "No milk entries found"
#         }), 404

#     return jsonify({
#         "milk_entries": result
#     })

# Get Milk Entries 
# by Customer ID & Date filter
@milk_entries.route("/milk-entries", methods=["GET"])
def get_milk_entries():
    
    customer_id = request.args.get("customer_id")
    entry_date = request.args.get("entry_date")
    entries = MilkEntry.query.filter_by(is_deleted=False)

    if customer_id:
        entries = entries.filter_by(
            customer_id=customer_id
        )
    
    if entry_date:
        entries = entries.filter_by(
           entry_date=entry_date
        )
    
    milk_entries = entries.all()

    all_entries = []
    for milk_entry in milk_entries:
        all_entries.append(milk_entry.to_dict())
        
    return jsonify({
        "milk_entries": all_entries
    })

# Get Single Milk Entry
@milk_entries.route("/milk-entries/<int:id>", methods=["GET"])
def get_milk_entry(id):

    milk_entry = MilkEntry.query.filter_by(id=id,is_deleted=False).first()

    if not milk_entry:
        return jsonify({
            "message": "Milk Entry not found"
        }), 404

    return jsonify(milk_entry.to_dict())


# Update Milk Entry
@milk_entries.route("/milk-entries/<int:id>", methods=["PUT"])
def update_milk_entry(id):

    milk_entry = MilkEntry.query.filter_by(id=id,is_deleted=False).first()

    if not milk_entry:
        return jsonify({
            "message": "Milk Entry not found"
        }), 404
    
    data = request.get_json()
    
    morning_qty = float(data.get("morning_qty",0))
    evening_qty = float(data.get("evening_qty",0))
     
    total_qty = morning_qty + evening_qty

    rate = float(milk_entry.rate)

    amount = total_qty * rate

    # updation
    milk_entry.morning_qty = morning_qty
    milk_entry.evening_qty = evening_qty
    milk_entry.total_qty = total_qty
    milk_entry.amount = amount

    db.session.commit()

    return jsonify({
        "message": "Milk Entry updated successfully",
        "milk_entry_id": milk_entry.id
    })


# Delete MilkEntry
@milk_entries.route("/milk-entries/<int:id>", methods=["DELETE"])
def delete_milk_entry(id):

    milk_entry = MilkEntry.query.filter_by(id=id,is_deleted=False).first()

    if not milk_entry:
        return jsonify({
            "message": "Milk Entry not found"
        }), 404

    # soft deletion
    milk_entry.is_deleted = True
    db.session.commit()

    return jsonify({
        "message": "Milk Entry deleted successfully",
        "milk_entry_id": milk_entry.id
    })

