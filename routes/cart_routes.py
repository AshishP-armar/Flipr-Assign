from flask import Blueprint, request, jsonify
from models import Cart, Product, db
from flask_jwt_extended import jwt_required, get_jwt_identity

cart_bp = Blueprint('cart', __name__)

# from flask import Blueprint

@cart_bp.route('cart/delete', methods=['OPTIONS'])
def handle_preflight():
    return '', 204




@cart_bp.route('cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    print(user_id)
    data = request.get_json()
    product_id, quantity = data['product_id'], data['quantity']
    print(product_id,quantity)
    if quantity <= 0:
        return jsonify({'error': 'Quantity must be a positive integer'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({'message': 'Product added to cart successfully'}), 201


@cart_bp.route('cart/update', methods=['PUT'])
@jwt_required()
def update_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id, new_quantity = data['product_id'], data['quantity']

    if new_quantity < 0:
        return jsonify({'error': 'Quantity cannot be negative'}), 400

    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not cart_item:
        return jsonify({'error': 'Product not found in cart'}), 404

    if new_quantity == 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = new_quantity

    db.session.commit()
    return jsonify({'message': 'Cart updated successfully'}), 200


@cart_bp.route('cart/delete', methods=['DELETE'])
@jwt_required()
def delete_from_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data['product_id']

    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not cart_item:
        return jsonify({'error': 'Product not found in cart'}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Product removed from cart successfully'}), 200


@cart_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return jsonify({'message': 'Your cart is empty'}), 404

    cart_details = []
    total_amount = 0

    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product:
            item_total = item.quantity * product.price
            total_amount += item_total
            cart_details.append({
                'product_id': product.id,
                'name': product.name,
                'quantity': item.quantity,
                'price': product.price,
                'total': item_total
            })

    return jsonify({
        'cart': cart_details,
        'total_amount': total_amount
    }), 200