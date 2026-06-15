from flask import Blueprint, request, jsonify
from extensions import db
from models.products import Product

products = Blueprint("product", __name__)

# Create Product
@products.route("/products",methods=["POST"])
def create_product():

    data = request.get_json()

    product = Product(
        name = data["name"],
        unit = data["unit"],
        rate = data["rate"]
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "Product created successfully",
        "product_id": product.id
    }), 201


# Get All Products
@products.route("/products", methods=["GET"])
def get_products():

    products = Product.query.filter_by(is_deleted=False).all()

    result = []

    for product in products:
        result.append(product.to_dict())

    if not result:
        return jsonify({
            "message": "No products found"
        }), 404

    return jsonify({
        "products": result
    })


# Get Single products
@products.route("/products/<int:id>", methods=["GET"])
def get_product(id):

    product = Product.query.filter_by(id=id,is_deleted=False).first()

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    return jsonify(product.to_dict())


# Update products
@products.route("/products/<int:id>", methods=["PUT"])
def update_product(id):

    product = Product.query.filter_by(id=id,is_deleted=False).first()

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404
    
    data = request.get_json()
    product.name = data["name"]
    product.unit = data["unit"]
    product.rate = data["rate"]

    db.session.commit()

    return jsonify({
        "message": "Product updated successfully",
        "product_id": product.id
    })


# Delete Product
@products.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):

    product = Product.query.filter_by(id=id,is_deleted=False).first()

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    # soft deletion
    product.is_deleted = True
    db.session.commit()

    return jsonify({
        "message": "Product deleted successfully",
        "product_id": product.id
    })