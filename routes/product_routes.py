from flask import Blueprint, request, jsonify,session
from models import Product, db
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity,jwt_required
from models import User



product_bp = Blueprint('product', __name__)

@product_bp.route('/addproduct', methods=['POST'])
def add_product():
    data = request.get_json()

    # Validate that all required fields are provided
    required_fields = ['name', 'description', 'price', 'category']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'error': f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Extract fields from the data
    name = data['name']
    description = data['description']
    price = data['price']
    category = data['category']

    # Validate price (should be a positive number)
    try:
        price = float(price)
        if price <= 0:
            return jsonify({'error': 'Price must be a positive number'}), 400
    except ValueError:
        return jsonify({'error': 'Price must be a valid number'}), 400

    # Add the new product to the database
    new_product = Product(name=name, description=description, price=price, category=category)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product added successfully', 'product_id': new_product.id}), 201

@product_bp.route('/updateproduct/<int:product_id>', methods=['PUT'])

def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.category = data.get('category', product.category)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'}), 200

@product_bp.route('/deleteproduct/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200

@product_bp.route('/products', methods=['GET'])
@jwt_required()
def get_all_products():
    current_user = User.query.filter_by(id=get_jwt_identity()).first()
   
   
    # Check if the user is an admin
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    products = Product.query.all()
    if not products:
        return jsonify({'message': 'No products found'}), 404
    print(session.get('is_admin'))
    print(session.get("user_id"))
    print(products)
    
    return jsonify({'products': [{'id': p.id, 'name': p.name, 'price': p.price,'description':p.description} for p in products]}), 200