from flask import Blueprint, request, jsonify
from extensions import db
from models.milk_entry import MilkEntry

milk_entries = Blueprint("milk_entries", __name__)

# Create Milk Entry
@milk_entries.route("/",methods=["POST"])
def create_milk_entry():

    data = request.get_json()

    milk_entry = MilkEntry(
       data[""]
    )

    db.session.add(milk_entry)
    db.session.commit()

    return jsonify({
        "message": "MilkEntry created successfully",
        "milk_entry_id": milk_entry.id
    }), 201


# Get All MilkEntries
@milk_entries.route("/milk_entrys", methods=["GET"])
def get_milk_entrys():

    milk_entries = MilkEntry.query.filter_by(is_deleted=False).all()

    result = []

    for milk_entry in milk_entries:
        result.append(milk_entry.to_dict())

    if not result:
        return jsonify({
            "message": "No milk entries found"
        }), 404

    return jsonify({
        "milk_entries": result
    })


# Get Single MilkEntry
@milk_entries.route("/milk_entrys/<int:id>", methods=["GET"])
def get_milk_entry(id):

    milk_entry = MilkEntry.query.filter_by(id=id,is_deleted=False).first()

    if not milk_entry:
        return jsonify({
            "message": "MilkEntry not found"
        }), 404

    return jsonify(milk_entry.to_dict())


# Update MilkEntry
@milk_entries.route("/milk_entrys/<int:id>", methods=["PUT"])
def update_milk_entry(id):

    milk_entry = MilkEntry.query.filter_by(id=id,is_deleted=False).first()

    if not milk_entry:
        return jsonify({
            "message": "MilkEntry not found"
        }), 404
    
    data = request.get_json()
    milk_entry.unit = data["unit"]
    milk_entry.rate = data["rate"]

    db.session.commit()

    return jsonify({
        "message": "MilkEntry updated successfully",
        "milk_entry_id": milk_entry.id
    })


# Delete MilkEntry
@milk_entries.route("/milk_entrys/<int:id>", methods=["DELETE"])
def delete_milk_entry(id):

    milk_entry = MilkEntry.query.filter_by(id=id,is_deleted=False).first()

    if not milk_entry:
        return jsonify({
            "message": "MilkEntry not found"
        }), 404

    # soft deletion
    milk_entry.is_deleted = True
    db.session.commit()

    return jsonify({
        "message": "MilkEntry deleted successfully",
        "milk_entry_id": milk_entry.id
    })